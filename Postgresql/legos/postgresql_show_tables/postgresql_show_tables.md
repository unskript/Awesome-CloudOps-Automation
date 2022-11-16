{
  "action_title": "Show tables in PostgreSQL Database",
  "action_description": "Show the tables existing in a PostgreSQL Database. We execute the following query to fetch this information SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';",
  "action_type": "LEGO_TYPE_POSTGRESQL",
  "action_entry_function": "postgresql_show_tables",
  "action_needs_credential": true,
  "action_supports_poll": true,
  "action_supports_iteration": true,
  "action_output_type": "ACTION_OUTPUT_TYPE_LIST",
  "action_verbs": [
    "fetch",
    "get",
    "show",
    "display",
    "list"
  ],
  "action_nouns": [
    "postgresql",
    "sql",
    "tables"
  ]
}
