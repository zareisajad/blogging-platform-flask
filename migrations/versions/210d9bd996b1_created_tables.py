"""created tables

Revision ID: 210d9bd996b1
Revises: 
Create Date: 2021-12-19 16:12:35.275112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '210d9bd996b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('avatar', sa.String(length=200), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=200), nullable=True),
    sa.Column('title', sa.String(length=300), nullable=True),
    sa.Column('tags', sa.String(length=600), nullable=True),
    sa.Column('content', sa.String(length=800), nullable=True),
    sa.Column('view', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_create_date'), 'post', ['create_date'], unique=False)
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fname', sa.String(length=120), nullable=True),
    sa.Column('lname', sa.String(length=120), nullable=True),
    sa.Column('about', sa.String(length=250), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=300), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_create_date'), 'comment', ['create_date'], unique=False)
    op.create_table('post_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_like')
    op.drop_index(op.f('ix_comment_create_date'), table_name='comment')
    op.drop_table('comment')
    op.drop_table('profile')
    op.drop_index(op.f('ix_post_create_date'), table_name='post')
    op.drop_table('post')
    op.drop_table('followers')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###