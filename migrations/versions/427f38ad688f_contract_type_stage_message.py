"""contract type stage message

Revision ID: 427f38ad688f
Revises: 17ba496fb5ee
Create Date: 2015-08-26 14:57:09.122352

"""

# revision identifiers, used by Alembic.
revision = '427f38ad688f'
down_revision = '17ba496fb5ee'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    contract_type = op.create_table('contract_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.bulk_insert(
        contract_type,
        [
            { 'name': 'PBOE' }, { 'name': 'PWSA' }, { 'name': 'CWCOG' }, { 'name': 'ELA' },
            { 'name': 'B-BID' }, { 'name': 'U.R.A.' }, { 'name': 'GSA' }, { 'name': 'County' },
            { 'name': 'A-BID' }, { 'name': 'Lackawanna' }, { 'name': 'Philadelphia' },
            { 'name': 'STATE' }, { 'name': 'COSTARS' }
        ]
    )


    op.create_index(op.f('ix_contract_type_id'), 'contract_type', ['id'], unique=False)
    op.add_column('contract', sa.Column('contract_type_id', sa.Integer(), nullable=True))

    op.execute(
        sa.sql.text(
            '''
            UPDATE contract SET contract_type_id = (
                SELECT id from contract_type WHERE contract.contract_type = contract_type.name
            )
            '''
        )
    )

    op.create_foreign_key('contract_id_contract_type_contract_id_fkey', 'contract', 'contract_type', ['contract_type_id'], ['id'])
    op.drop_column('contract', 'contract_type')
    op.add_column('stage', sa.Column('default_message', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stage', 'default_message')
    op.add_column('contract', sa.Column('contract_type', sa.VARCHAR(length=255), autoincrement=False, nullable=True))

    op.execute(
        sa.sql.text(
            '''
            UPDATE contract SET contract_type = (
                SELECT name from contract_type WHERE contract.contract_type_id = contract_type.id
            )
            '''
        )
    )

    op.drop_constraint('contract_id_contract_type_contract_id_fkey', 'contract', type_='foreignkey')
    op.drop_column('contract', 'contract_type_id')
    op.drop_index(op.f('ix_contract_type_id'), table_name='contract_type')
    op.drop_table('contract_type')
    ### end Alembic commands ###