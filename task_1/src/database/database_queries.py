create_cart_table = "CREATE TABLE \"cart\" ( id varchar PRIMARY KEY NOT NULL );"  # noqa
create_item_table = "CREATE TABLE \"item\" ( external_id varchar, name varchar, value integer, cart_id varchar, PRIMARY KEY (external_id, cart_id) );"  # noqa
create_cart = "INSERT INTO cart ( id ) VALUES ( \'{}\' );"  # noqa
create_item = "INSERT INTO item ( external_id, name, value, cart_id ) VALUES ( \'{}\', NULLIF (\'{}\', 'None'), CAST(NULLIF(\'{}\', 'None') AS INTEGER), \'{}\' );"  # noqa
update_item = "UPDATE item SET name=COALESCE(\'{}\', name),value=COALESCE({}, value) WHERE item.external_id=\'{}\' AND item.cart_id=\'{}\';"  # noqa
get_item = "SELECT * FROM item WHERE item.external_id=\'{}\' AND item.cart_id=\'{}\';"  # noqa
