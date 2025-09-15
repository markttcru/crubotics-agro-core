from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('robots',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('robot_uid', sa.String(length=64), nullable=False, unique=True),
        sa.Column('name', sa.String(length=128)),
        sa.Column('status', sa.String(length=32), server_default='idle'),
        sa.Column('farm_id', sa.Integer()),
        sa.Column('farmer_name', sa.String(length=128)),
        sa.Column('battery_pct', sa.Float()),
        sa.Column('last_seen', sa.DateTime()),
        sa.Column('notes', sa.Text(), server_default='')
    )
    op.create_table('tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('kind', sa.String(length=64), nullable=False),
        sa.Column('crop', sa.String(length=64)),
        sa.Column('acres', sa.Float(), server_default='0.0'),
        sa.Column('farm_id', sa.Integer()),
        sa.Column('priority', sa.Integer(), server_default='5'),
        sa.Column('status', sa.String(length=32), server_default='queued'),
        sa.Column('scheduled_for', sa.DateTime()),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.Column('robot_id', sa.Integer(), sa.ForeignKey('robots.id'), nullable=True),
        sa.Column('payload', sa.Text(), server_default='{}')
    )
    op.create_table('telemetry',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('robot_id', sa.Integer(), sa.ForeignKey('robots.id', ondelete='CASCADE'), nullable=False),
        sa.Column('ts', sa.DateTime()),
        sa.Column('battery_pct', sa.Float()),
        sa.Column('lat', sa.Float()),
        sa.Column('lon', sa.Float()),
        sa.Column('soil_moisture', sa.Float()),
        sa.Column('temperature_c', sa.Float()),
        sa.Column('task_status', sa.String(length=64)),
        sa.Column('extra', sa.Text(), server_default='{}')
    )

def downgrade():
    op.drop_table('telemetry')
    op.drop_table('tasks')
    op.drop_table('robots')
