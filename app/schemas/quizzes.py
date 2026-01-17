from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, model_validator


class QuizQuestion(BaseModel):
    """Represents a single MCQ question inside a quiz."""

    # The question text itself - allows any string (text, numbers, formulas, etc.)
    question: str = Field(..., min_length=1, json_schema_extra={"example": "What is 2 + 2?"})

    # Multiple options for MCQ (2 to 4 options required) - each option can be any string
    options: list[str] = Field(..., min_length=2, max_length=4, json_schema_extra={"example": ["3", "4", "5", "6"]})

    # The correct answer (must match one of the options exactly)
    answer: str = Field(..., json_schema_extra={"example": "4"})

    @model_validator(mode="after")
    def validate_answer_in_options(self):
        """Ensure the correct answer matches exactly one of the options."""
        if self.answer not in self.options:
            raise ValueError(
                f"Correct answer '{self.answer}' must match one of the options: {self.options}"
            )
        return self

class QuizCreate(BaseModel):
    """Schema for creating a new quiz."""

    # IDs of related entities (validated later in router)
    courseId: str
    courseName: str  # Course name for display purposes
    teacherId: str
    tenantId: str

    # Basic quiz metadata
    quizNumber: int = Field(..., ge=1)
    description: Optional[str] = None
    dueDate: datetime

    # List of MCQ questions
    questions: list[QuizQuestion]

    # Optional time limit (in minutes)
    timeLimitMinutes: Optional[int] = Field(None, ge=1)

    # Required total marks for quiz
    totalMarks: int = Field(..., ge=1)

    # Whether quiz was generated using AI
    aiGenerated: Optional[bool] = False


class QuizUpdate(BaseModel):
    """Schema for updating an existing quiz. All fields are optional."""
    quizNumber: Optional[int] = None
    description: Optional[str] = None
    dueDate: Optional[datetime] = None
    questions: Optional[list[QuizQuestion]] = None
    timeLimitMinutes: Optional[int] = None
    totalMarks: Optional[int] = None
    aiGenerated: Optional[bool] = None

    # Allows disabling quiz (soft delete style)
    status: Optional[str] = Field(None, json_schema_extra={"example": "inactive"})

    @model_validator(mode="before")
    def convert_empty_strings(cls, data):
        if isinstance(data, dict):
            for k, v in data.items():
                if v == "":
                    data[k] = None
        return data

class QuizResponse(BaseModel):
    """Schema returned to client after create/get/update."""
    id: str
    courseId: str
    courseName: Optional[str] = None
    teacherId: str
    tenantId: str
    quizNumber: int
    description: Optional[str]
    dueDate: datetime
    questions: list[QuizQuestion]
    timeLimitMinutes: Optional[int]
    totalMarks: int
    aiGenerated: bool
    status: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None
