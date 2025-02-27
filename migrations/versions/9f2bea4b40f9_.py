"""empty message

Revision ID: 9f2bea4b40f9
Revises: e17316a5748b
Create Date: 2025-02-24 09:56:59.351083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f2bea4b40f9'
down_revision = 'e17316a5748b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('about_me',
               existing_type=sa.TEXT(),
               type_=sa.String(length=140),
               existing_nullable=True)
        batch_op.alter_column('last_seen',
               existing_type=sa.TEXT(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('last_seen',
               existing_type=sa.DateTime(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('about_me',
               existing_type=sa.String(length=140),
               type_=sa.TEXT(),
               existing_nullable=True)

    op.drop_table('followers')
    # ### end Alembic commands ###
