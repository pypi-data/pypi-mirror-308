from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from documente_shared.domain.enums import (
    DocumentProcessStatus,
    DocumentProcessSubCategory,
    DocumentProcessCategory,
)


@dataclass
class DocumentProcess(object):
    digest: str
    status: DocumentProcessStatus
    file_path: str
    file_bytes: Optional[bytes] = None
    category: Optional[DocumentProcessCategory] = None
    sub_category: Optional[DocumentProcessSubCategory] = None
    processed_csv_path: Optional[str] = None
    processed_csv_bytes: Optional[bytes] = None
    processed_xlsx_path: Optional[str] = None
    processed_xlsx_bytes: Optional[bytes] = None
    processing_time: Optional[Decimal] = None
    uploded_at: Optional[datetime] = None
    enqueued_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def is_pending(self) -> bool:
        return self.status == DocumentProcessStatus.PENDING

    @property
    def is_enqueued(self) -> bool:
        return self.status == DocumentProcessStatus.ENQUEUED

    @property
    def is_processing(self) -> bool:
        return self.status == DocumentProcessStatus.PROCESSING

    @property
    def is_completed(self) -> bool:
        return self.status == DocumentProcessStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self.status == DocumentProcessStatus.FAILED

    @property
    def is_valid(self) -> bool:
        return all([
            self.digest,
            self.status,
            self.file_path,
        ])

    def enqueue(self):
        self.status = DocumentProcessStatus.ENQUEUED
        self.enqueued_at = datetime.now()

    def processing(self):
        self.status = DocumentProcessStatus.PROCESSING
        self.started_at = datetime.now()

    def failed(self):
        self.status = DocumentProcessStatus.FAILED
        self.failed_at = datetime.now()

    def completed(self):
        self.status = DocumentProcessStatus.COMPLETED
        self.completed_at = datetime.now()

    def deleted(self):
        self.status = DocumentProcessStatus.DELETED

    @property
    def filename(self) -> str:
        filename_with_extension = self.file_path.split('/')[-1]
        return filename_with_extension.split('.')[0]

    @property
    def to_dict(self) -> dict:
        return {
            'digest': self.digest,
            'status': self.status.value,
            'file_path': self.file_path,
            'category': (
                str(self.category)
                if self.category else None
            ),
            'sub_category': (
                str(self.sub_category)
                if self.sub_category else None
            ),
            'processed_csv_path': self.processed_csv_path,
            'processed_xlsx_path': self.processed_xlsx_path,
            'processing_time': (
                str(self.processing_time)
                if self.processing_time else None
            ),
            'uploded_at': self.uploded_at.isoformat() if self.uploded_at else None,
            'enqueued_at': self.enqueued_at.isoformat() if self.enqueued_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'failed_at': self.failed_at.isoformat() if self.failed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DocumentProcess':
        return cls(
            digest=data.get('digest'),
            status=DocumentProcessStatus.from_value(data.get('status')),
            file_path=data.get('file_path'),
            category=(
                DocumentProcessCategory.from_value(data.get('category'))
                if data.get('category') else None
            ),
            sub_category=(
                DocumentProcessSubCategory.from_value(data.get('sub_category'))
                if data.get('sub_category') else None
            ),
            processed_csv_path=data.get('processed_csv_path'),
            processed_xlsx_path=data.get('processed_xlsx_path'),
            processing_time=(
                Decimal(data.get('processing_time'))
                if data.get('processing_time') else None
            ),
            uploded_at=(
                datetime.fromisoformat(data.get('uploded_at'))
                if data.get('uploded_at') else None
            ),
            enqueued_at=(
                datetime.fromisoformat(data.get('enqueued_at'))
                if data.get('enqueued_at') else None
            ),
            started_at=(
                datetime.fromisoformat(data.get('started_at'))
                if data.get('started_at') else None
            ),
            failed_at=(
                datetime.fromisoformat(data.get('failed_at'))
                if data.get('failed_at') else None
            ),
            completed_at=(
                datetime.fromisoformat(data.get('completed_at'))
                if data.get('processed_at') else None
            ),
        )