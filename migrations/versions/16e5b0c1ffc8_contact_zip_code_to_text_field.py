"""contact zip code to text field

Revision ID: 16e5b0c1ffc8
Revises: 8ac7c042469
Create Date: 2015-10-12 15:23:39.600694

"""

# revision identifiers, used by Alembic.
revision = '16e5b0c1ffc8'
down_revision = '8ac7c042469'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(u'opportunity', 'created_by_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text(u'1'))
    op.create_foreign_key('opportunity_created_from_id_contract_id_fkey',
        'opportunity', 'contract', ['created_from_id'], ['id']
    )
    op.alter_column(u'company_contact', 'zip_code',
      existing_type=sa.INTEGER(),
      type_=sa.VARCHAR(255),
      nullable=True
    )
    ### end Alembic commands ###

    op.execute(
        sa.sql.text(
            '''
            UPDATE company_contact
            SET zip_code = rpad('0', 5, zip_code)
            where char_length(zip_code) < 5
            '''
        )
    )

def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute(
      sa.sql.text(
        '''ALTER TABLE company_contact ALTER COLUMN zip_code TYPE integer USING (trim(zip_code)::integer)
        '''
      )
    )
    op.drop_constraint('opportunity_created_from_id_contract_id_fkey',
        'opportunity', type_='foreignkey'
    )
    op.alter_column(u'opportunity', 'created_by_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text(u'1'))
    ### end Alembic commands ###