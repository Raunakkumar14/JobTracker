"""create jobs table

Revision ID: 9b3f5c7d2a6e
Revises: 3371b330ba7e
Create Date: 2026-06-27 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "9b3f5c7d2a6e"
down_revision = "3371b330ba7e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            company VARCHAR NOT NULL,
            description TEXT,
            location VARCHAR,
            deadline DATE,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users(id)
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS jobs")
