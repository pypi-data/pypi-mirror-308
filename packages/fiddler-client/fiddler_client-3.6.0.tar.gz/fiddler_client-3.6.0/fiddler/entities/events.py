from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any, Callable
from uuid import UUID

import pandas as pd
from requests import Response
from tqdm import tqdm

from fiddler.configs import STREAM_EVENT_LIMIT
from fiddler.connection import ConnectionMixin
from fiddler.decorators import handle_api_error
from fiddler.entities.file import File
from fiddler.entities.job import Job
from fiddler.schemas.dataset import EnvType
from fiddler.schemas.events import EventsSource, FileSource
from fiddler.schemas.job import JobCompactResp
from fiddler.utils.logger import get_logger

logger = get_logger(__name__)


class EventPublisher(ConnectionMixin):
    STREAM_LIMIT = STREAM_EVENT_LIMIT

    def __init__(self, model_id: UUID) -> None:
        """
        Event publishing methods

        :param model_id: Model identifier
        """
        self.model_id = model_id

    @handle_api_error
    def publish(
        self,
        source: list[dict[str, Any]] | str | Path | pd.DataFrame,
        environment: EnvType = EnvType.PRODUCTION,
        dataset_name: str | None = None,
        update: bool = False,
    ) -> list[UUID] | Job:
        """
        Publish Pre-production or Production data

        :param source: one of:
            Path or str path: path for data file.
            dataframe: events dataframe.
            list[dict]: list of event dicts EnvType.PRE_PRODUCTION is not supported
        :param environment: Either EnvType.PRE_PRODUCTION or EnvType.PRODUCTION
        :param dataset_name: Name of the dataset. Not supported for EnvType.PRODUCTION
        :param update: flag indicating if the events are updates to previously published rows

        :return: list[UUID] for list of dicts source and Job object for file path or dataframe source.
        """

        publish_method = self._get_publish_method(source=source)

        return publish_method(
            source=source,
            environment=environment,
            dataset_name=dataset_name,
            update=update,
        )

    def _get_publish_method(
        self, source: list[dict[str, Any]] | str | Path | pd.DataFrame
    ) -> Callable:
        if isinstance(source, (str, Path)):
            return self._publish_file

        if isinstance(source, pd.DataFrame):
            return self._publish_df

        if isinstance(source, list):
            return self._publish_stream

        raise ValueError(f'Unsupported source - {type(source)}')

    def _publish_df(
        self,
        source: pd.DataFrame,
        environment: EnvType,
        dataset_name: str | None = None,
        update: bool = False,
    ) -> Job:
        temp_file = tempfile.NamedTemporaryFile(suffix='.parquet', delete=False)
        try:
            source.to_parquet(temp_file.name, index=False)
            job = self._publish_file(
                source=temp_file.name,
                environment=environment,
                dataset_name=dataset_name,
                update=update,
            )
            temp_file.close()
            return job

        except Exception:
            logger.warning(
                'Failed to convert input dataframe to parquet format. Retrying as a CSV file.'
            )

        finally:
            os.unlink(temp_file.name)

        # Trying as csv file as source could not be converted to parquet
        try:
            temp_file = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
            source.to_csv(temp_file.name, index=False)
            job = self._publish_file(
                source=temp_file.name,
                environment=environment,
                dataset_name=dataset_name,
                update=update,
            )
            temp_file.close()
        finally:
            os.unlink(temp_file.name)
        return job

    def _publish_stream(
        self,
        source: list[dict[str, Any]],
        environment: EnvType = EnvType.PRODUCTION,
        dataset_name: str | None = None,
        update: bool = False,
    ) -> list[UUID]:
        event_ids = []
        for i in tqdm(range(0, len(source), self.STREAM_LIMIT)):
            response = self._publish_call(
                source=EventsSource(events=source[i : i + self.STREAM_LIMIT]),
                environment=environment,
                dataset_name=dataset_name,
                update=update,
            )
            event_ids.extend(response.json()['data']['event_ids'])

        return event_ids

    def _publish_file(
        self,
        source: Path | str,
        environment: EnvType,
        dataset_name: str | None = None,
        update: bool = False,
    ) -> Job:
        file = File(path=Path(source)).upload()

        assert file.id is not None

        response = self._publish_call(
            source=FileSource(file_id=file.id),
            environment=environment,
            dataset_name=dataset_name,
            update=update,
        )
        job_compact = JobCompactResp(**response.json()['data']['job'])
        return Job.get(id_=job_compact.id)

    def _publish_call(
        self,
        source: FileSource | EventsSource,
        environment: EnvType,
        dataset_name: str | None = None,
        update: bool = False,
    ) -> Response:
        if update:
            method = self._client().patch
        else:
            method = self._client().post
        return method(
            url='/v3/events',
            data={
                'source': source.dict(),
                'model_id': self.model_id,
                'env_type': environment,
                'env_name': dataset_name,
            },
        )
