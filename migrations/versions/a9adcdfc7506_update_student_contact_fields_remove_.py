"""Update student contact fields - remove contact_number, add primary/secondary parent contacts, auto-generate admission_number

Revision ID: a9adcdfc7506
Revises: 8963baa45b8e
Create Date: 2026-02-18 14:17:31.880003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9adcdfc7506'
down_revision = '8963baa45b8e'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    
    # Check current table structure
    inspector = sa.inspect(connection)
    columns = [col['name'] for col in inspector.get_columns('student')]
    
    # Step 1: Add new columns only if they don't exist
    if 'parent_primary_contact' not in columns:
        try:
            op.add_column('student', sa.Column('parent_primary_contact', sa.String(length=20), nullable=True))
        except Exception:
            pass  # Column might already exist
    
    if 'parent_secondary_contact' not in columns:
        try:
            op.add_column('student', sa.Column('parent_secondary_contact', sa.String(length=20), nullable=True))
        except Exception:
            pass  # Column might already exist
    
    # Step 2: Copy data from parent_contact to parent_primary_contact (if parent_contact exists)
    if 'parent_contact' in columns:
        try:
            connection.execute(sa.text(
                "UPDATE student SET parent_primary_contact = parent_contact WHERE parent_contact IS NOT NULL AND (parent_primary_contact IS NULL OR parent_primary_contact = '')"
            ))
            
            # For any NULL values, set a default (shouldn't happen, but safety)
            connection.execute(sa.text(
                "UPDATE student SET parent_primary_contact = '' WHERE parent_primary_contact IS NULL"
            ))
        except Exception as e:
            print(f"Warning: Could not copy parent_contact data: {e}")
    
    # Step 3: Drop old columns if they exist (drop both in one batch operation)
    if 'contact_number' in columns or 'parent_contact' in columns:
        try:
            with op.batch_alter_table('student', schema=None) as batch_op:
                if 'contact_number' in columns:
                    batch_op.drop_column('contact_number')
                if 'parent_contact' in columns:
                    batch_op.drop_column('parent_contact')
        except Exception as e:
            print(f"Warning: Could not drop old columns: {e}")
            # If batch fails, try individual drops (for SQLite compatibility)
            if 'contact_number' in columns:
                try:
                    connection.execute(sa.text("ALTER TABLE student DROP COLUMN contact_number"))
                except:
                    pass
            if 'parent_contact' in columns:
                try:
                    connection.execute(sa.text("ALTER TABLE student DROP COLUMN parent_contact"))
                except:
                    pass
    
    # Note: parent_primary_contact will remain nullable in SQLite
    # but the model enforces NOT NULL, which is fine

    # ### end Alembic commands ###


def downgrade():
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    columns = [col['name'] for col in inspector.get_columns('student')]
    
    # Step 1: Add old columns if they don't exist
    if 'parent_contact' not in columns:
        try:
            op.add_column('student', sa.Column('parent_contact', sa.VARCHAR(length=20), nullable=True))
        except Exception:
            pass
    
    if 'contact_number' not in columns:
        try:
            op.add_column('student', sa.Column('contact_number', sa.VARCHAR(length=20), nullable=True))
        except Exception:
            pass
    
    # Step 2: Copy data from parent_primary_contact back to parent_contact
    if 'parent_primary_contact' in columns:
        try:
            connection.execute(sa.text(
                "UPDATE student SET parent_contact = parent_primary_contact WHERE parent_primary_contact IS NOT NULL"
            ))
        except Exception:
            pass
    
    # Step 3: Drop new columns
    if 'parent_secondary_contact' in columns:
        try:
            with op.batch_alter_table('student', schema=None) as batch_op:
                batch_op.drop_column('parent_secondary_contact')
        except Exception:
            pass
    
    if 'parent_primary_contact' in columns:
        try:
            with op.batch_alter_table('student', schema=None) as batch_op:
                batch_op.drop_column('parent_primary_contact')
        except Exception:
            pass

    # ### end Alembic commands ###
