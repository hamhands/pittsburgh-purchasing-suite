"""roles_many_to_many

Revision ID: 444872e13dac
Revises: 31d29fbffe44
Create Date: 2016-01-21 00:49:50.100482

"""

# revision identifiers, used by Alembic.
revision = '444872e13dac'
down_revision = '31d29fbffe44'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.drop_constraint(u'users_role_id_fkey', 'users', type_='foreignkey')

    op.execute(sa.sql.text('''
        INSERT INTO roles_users
        SELECT id, role_id FROM users where role_id is not null
    '''))

    op.drop_column(u'users', 'role_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'users', sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'users_role_id_fkey', 'users', 'roles', ['role_id'], ['id'])

    op.execute(sa.sql.text('''
        UPDATE users SET role_id =
        (select min(role_id) from roles_users
            where users.id = roles_users.user_id)
    '''))

    op.drop_table('roles_users')
    ### end Alembic commands ###
