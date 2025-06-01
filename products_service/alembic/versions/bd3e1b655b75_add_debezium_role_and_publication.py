"""Add Debezium role and publication

Revision ID: bd3e1b655b75
Revises: 362f21613334
Create Date: 2025-06-01 02:17:33.549598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd3e1b655b75'
down_revision: Union[str, None] = '362f21613334'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create Debezium role if it doesn't already exist
    op.execute("DO $$ BEGIN "
               "IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'debezium') THEN "
               "CREATE ROLE debezium WITH REPLICATION LOGIN PASSWORD 'password'; "
               "END IF; "
               "END $$;")

    # Create publication if it doesn't already exist
    op.execute("DO $$ BEGIN "
               "IF NOT EXISTS (SELECT 1 FROM pg_publication WHERE pubname = 'debezium_pub') THEN "
               "CREATE PUBLICATION debezium_pub FOR TABLE public.products; "
               "END IF; "
               "END $$;")


def downgrade() -> None:
    """Downgrade schema."""
    # Drop publication (if exists)
    op.execute("DROP PUBLICATION IF EXISTS debezium_pub;")

    # Drop role (optional, if safe)
    op.execute("DROP ROLE IF EXISTS debezium;")
