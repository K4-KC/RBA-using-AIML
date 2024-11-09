ABLE IF EXISTS rba; """
c.execute(drop_table)

create_table = """ CREATE TABLE IF NOT EXISTS rba (
    User_ID BIGINT,
    Is_Account_Takeover BOOL
); """
c.execute(create_table)