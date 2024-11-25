# ETL Example using duckdb

## Input Source

Data: [Reddit Comments about 4.2 GB](
https://huggingface.co/datasets/OpenCo7/UpVoteWeb/blob/main/data/merged_1.parquet)

~~~
% ls -l ~/Downloads/merged_1.parquet
-rw-r--r--@ 1 mparsian  staff  4272062254 Nov 24 18:58 /Users/mparsian/Downloads/merged_1.parquet

~~~

## duckdb session

~~~sql
duckdb_folder  % duckdb
v1.1.2 f680b7d08f
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.

D CREATE TABLE reddit_comments AS SELECT * FROM read_parquet('/Users/mparsian/Downloads/merged_1.parquet');
100% ▕████████████████████████████████████████████████████████████▏
D select * from reddit_comments limit 5;
┌─────────┬────────────┬─────────┬──────────────────────┬──────────────────────┬───┬─────────────┬─────────┬──────────┬────────────────┬────────────┐
│   id    │ parent_id  │ post_id │         text         │         url          │ … │ token_count │  kind   │ language │ language_score │ media_urls │
│ varchar │  varchar   │ varchar │       varchar        │       varchar        │   │    int64    │ varchar │ varchar  │     double     │  int32[]   │
├─────────┼────────────┼─────────┼──────────────────────┼──────────────────────┼───┼─────────────┼─────────┼──────────┼────────────────┼────────────┤
│ kfrxfcr │ t3_18vki9b │ 18vki9b │ "devsisters is so …  │ https://www.reddit…  │ … │          13 │ comment │ en       │         0.8768 │ []         │
│ kfrxfdj │ t3_18vlhgc │ 18vlhgc │ Omar Epps waiting …  │ https://www.reddit…  │ … │          19 │ comment │ en       │         0.8109 │ []         │
│ kfrxfde │ t3_18vkkxu │ 18vkkxu │ May 1899 be a bett…  │ https://www.reddit…  │ … │          15 │ comment │ en       │         0.9628 │ []         │
│ kfrxfda │ t3_18vkqmn │ 18vkqmn │ Just clean it up a…  │ https://www.reddit…  │ … │          32 │ comment │ en       │         0.9488 │ []         │
│ kfrxfdl │ t1_kfrwiiz │ 18vl745 │ Absolutely pleasan…  │ https://www.reddit…  │ … │          46 │ comment │ en       │         0.9757 │ []         │
├─────────┴────────────┴─────────┴──────────────────────┴──────────────────────┴───┴─────────────┴─────────┴──────────┴────────────────┴────────────┤
│ 5 rows                                                                                                                      14 columns (10 shown) │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D select count(*) from reddit_comments;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│     20841149 │
└──────────────┘


D DESCRIBE SELECT * from reddit_comments;
┌────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│  column_name   │ column_type │  null   │   key   │ default │  extra  │
│    varchar     │   varchar   │ varchar │ varchar │ varchar │ varchar │
├────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ id             │ VARCHAR     │ YES     │         │         │         │
│ parent_id      │ VARCHAR     │ YES     │         │         │         │
│ post_id        │ VARCHAR     │ YES     │         │         │         │
│ text           │ VARCHAR     │ YES     │         │         │         │
│ url            │ VARCHAR     │ YES     │         │         │         │
│ date           │ VARCHAR     │ YES     │         │         │         │
│ author         │ VARCHAR     │ YES     │         │         │         │
│ subreddit      │ VARCHAR     │ YES     │         │         │         │
│ score          │ BIGINT      │ YES     │         │         │         │
│ token_count    │ BIGINT      │ YES     │         │         │         │
│ kind           │ VARCHAR     │ YES     │         │         │         │
│ language       │ VARCHAR     │ YES     │         │         │         │
│ language_score │ DOUBLE      │ YES     │         │         │         │
│ media_urls     │ INTEGER[]   │ YES     │         │         │         │
├────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
│ 14 rows                                                    6 columns │
└──────────────────────────────────────────────────────────────────────┘
D SELECT author, sum(language_score) sum_of_language_score
      FROM reddit_comments
      GROUP BY author
      ORDER BY sum_of_language_score DESC;
100% ▕████████████████████████████████████████████████████████████▏
┌──────────────────────┬───────────────────────┐
│        author        │ sum_of_language_score │
│       varchar        │        double         │
├──────────────────────┼───────────────────────┤
│ [deleted]            │     968373.2668000124 │
│ AutoModerator        │     85628.46609999996 │
│ avatarbot            │             5157.3868 │
│ MTGCardFetcher       │    3206.6262999999994 │
│ RemindMeBot          │    1214.7445000000014 │
│ romance-bot          │    1211.1374999999996 │
│ SaveVideo            │    1168.7045000000007 │
│ sneakpeekbot         │             1136.4439 │
│ ApplePitou           │             1121.2204 │
│ exclaim_bot          │     929.4596000000001 │
│ alphabet_order_bot   │     809.4385999999998 │
│ ChrisRageIsBack      │     787.5195999999999 │
│ -SofaKingVote-       │     736.3642999999995 │
│ Paid-Not-Payed-Bot   │     736.0106000000002 │
│ vic2moh              │     719.9392000000003 │
│ _Noorie              │              706.0886 │
│ CatStroking          │     699.8692999999998 │
│ deport_racists_next  │     689.1381000000002 │
│ VettedBot            │     666.1939000000001 │
│ B0tRank              │     662.1663000000005 │
│   ·                  │                   ·   │
│   ·                  │                   ·   │
│   ·                  │                   ·   │
│ prakow               │                0.0475 │
│ BitRepresentative387 │                0.0475 │
│ Objective_Minimum_62 │                0.0475 │
│ Royal42Smallsy       │                0.0475 │
│ Professional_Deer_82 │                0.0463 │
│ OptionsJohnny        │                0.0463 │
│ wizardfromthem00n    │                0.0458 │
│ Kaynotfoundwastaken  │                0.0458 │
│ Raaz_s               │                0.0453 │
│ Nicklovin0571        │                0.0428 │
│ Massive_Claim_7931   │                 0.042 │
│ stockstosocks212     │                 0.042 │
│ Acidseyes420         │                 0.042 │
│ oh_my_gra            │                 0.042 │
│ DecentPerception6280 │                 0.042 │
│ Angelnoodlepup       │                 0.042 │
│ FriendlyAct4925      │                0.0378 │
│ Grouchy-Lynx4983     │                0.0313 │
│ KillerFusion1212     │                0.0313 │
│ Spiritual_Bath_9143  │                0.0313 │
├──────────────────────┴───────────────────────┤
│ 3558744 rows (40 shown)            2 columns │
└──────────────────────────────────────────────┘
D CREATE OR REPLACE TABLE most_recent_comment_per_author AS
      SELECT id, author, text, date
      FROM (
      SELECT id, author, text, date,
              ROW_NUMBER() OVER (PARTITION BY author ORDER BY date DESC) AS row_num
      FROM reddit_comments
      ) ranked_table
      WHERE row_num = 1;
100% ▕████████████████████████████████████████████████████████████▏
D select count(*) from most_recent_comment_per_author;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│      3558744 │
└──────────────┘
D select * from most_recent_comment_per_author limit 5;
┌─────────┬─────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────┬─────────────────────┐
│   id    │       author        │                                               text                                               │        date         │
│ varchar │       varchar       │                                             varchar                                              │       varchar       │
├─────────┼─────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────┤
│ kgmg0bq │ Bread_was_returned  │ Finished display termagant … for golden demon shelves!                                           │ 2024-01-06T19:29:07 │
│ kgjztzz │ Breadlarr           │ Dude you're getting there. Mad respect.                                                          │ 2024-01-06T07:05:51 │
│ kfuo0y5 │ BreakDesperate7637  │ "It's probably hideous and slow."  "Just like your dad."                                         │ 2024-01-01T17:01:17 │
│ kgj6ix7 │ BreakfastIndividual │ Go get Debrox it will help with your earwax buildup it's the best works out there GL...          │ 2024-01-06T02:57:10 │
│ kg7g4u7 │ BreakfastWeak4796   │ Don’t have as much time as I used to. Real life job and other adult responsibilities eat up mo…  │ 2024-01-04T00:20:57 │
└─────────┴─────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────┴─────────────────────┘
D COPY (SELECT * FROM most_recent_comment_per_author)
      TO '/tmp/output/'
      (format parquet, file_size_bytes '256MB', compression 'zstd', filename_pattern "{{uuid}}", overwrite_or_ignore true);

100% ▕████████████████████████████████████████████████████████████▏
D
D .exit
~~~

Examine saved/loaded files:

~~~
duckdb_folder  % ls -l /tmp/output/
total 639632
-rw-r--r--  1 mparsian  wheel   50986131 Nov 24 19:17 {31ec23f2-1fa4-4144-94cd-131f22d1976c}.parquet
-rw-r--r--  1 mparsian  wheel  260564214 Nov 24 19:17 {747f6d43-f41f-4ed4-9faa-2283d2d26110}.parquet
~~~

