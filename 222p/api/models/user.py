"""
User model for authentication and basic user information
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from config.database import Base

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """User model for authentication."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    onboarding_responses = relationship("OnboardingResponse", back_populates="user", cascade="all, delete-orphan")
    matches = relationship("Match", foreign_keys="Match.user_id", back_populates="user", cascade="all, delete-orphan")
    matched_by = relationship("Match", foreign_keys="Match.matched_user_id", back_populates="matched_user")
    created_events = relationship("Event", back_populates="creator")
    event_invitations = relationship("EventInvitation", back_populates="invitee")
    created_groups = relationship("Group", back_populates="created_by_user")
    group_memberships = relationship("GroupMembership", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.recipient_id", back_populates="recipient")
    moderation_reports = relationship("ModerationFlag", foreign_keys="ModerationFlag.reporter_id", back_populates="reporter")
    reported_by = relationship("ModerationFlag", foreign_keys="ModerationFlag.reported_user_id", back_populates="reported_user")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user")
    
    def set_password(self, password: str) -> None:
        """Hash and set password."""
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(password, self.password_hash)
    
    def is_locked(self) -> bool:
        """Check if account is locked."""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def increment_failed_login(self, lockout_minutes: int = 15) -> None:
        """Increment failed login attempts and lock if necessary."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # Max attempts
            self.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
    
    def reset_failed_login(self) -> None:
        """Reset failed login attempts and unlock account."""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = datetime.utcnow()
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', active={self.is_active})>"