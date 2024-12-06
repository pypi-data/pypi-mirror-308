BEGIN;
--
-- Create model Chapter
--
DROP TABLE IF EXISTS "chapters";
CREATE TABLE "chapters" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" varchar(16) NOT NULL UNIQUE,
  "order" integer NOT NULL UNIQUE,
  "type" bool NOT NULL,
  "verse_count" integer NOT NULL DEFAULT 1
);
DROP INDEX IF EXISTS "chapters_verse_count_5777cda7";
CREATE INDEX "chapters_verse_count_5777cda7" ON "chapters" ("verse_count");

--
-- Create model Part
--
DROP TABLE IF EXISTS "parts";
CREATE TABLE "parts" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" varchar(32) NOT NULL UNIQUE,
  "verse_count" integer NOT NULL DEFAULT 1
);
DROP INDEX IF EXISTS "parts_verse_count_9501296e";
CREATE INDEX "parts_verse_count_9501296e" ON "parts" ("verse_count");

--
-- Create model Group
--
DROP TABLE IF EXISTS "groups";
CREATE TABLE "groups" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" varchar(32) NOT NULL UNIQUE,
  "verse_count" integer NOT NULL DEFAULT 1,
  "part_id" bigint NULL REFERENCES "parts" ("id") DEFERRABLE INITIALLY DEFERRED
);
DROP INDEX IF EXISTS "groups_verse_count_cbf9c194";
CREATE INDEX "groups_verse_count_cbf9c194" ON "groups" ("verse_count");
DROP INDEX IF EXISTS "groups_part_id_5cc7ea42";
CREATE INDEX "groups_part_id_5cc7ea42" ON "groups" ("part_id");

--
-- Create model Quarter
--
DROP TABLE IF EXISTS "quarters";
CREATE TABLE "quarters" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" varchar(32) NOT NULL UNIQUE,
  "verse_count" integer NOT NULL DEFAULT 1,
  "group_id" bigint NULL REFERENCES "groups" ("id") DEFERRABLE INITIALLY DEFERRED,
  "part_id" bigint NULL REFERENCES "parts" ("id") DEFERRABLE INITIALLY DEFERRED
);
DROP INDEX IF EXISTS "quarters_verse_count_3da85c21";
CREATE INDEX "quarters_verse_count_3da85c21" ON "quarters" ("verse_count");
DROP INDEX IF EXISTS "quarters_group_id_425bbd82";
CREATE INDEX "quarters_group_id_425bbd82" ON "quarters" ("group_id");
DROP INDEX IF EXISTS "quarters_part_id_ffd45a90";
CREATE INDEX "quarters_part_id_ffd45a90" ON "quarters" ("part_id");

--
-- Create model Page
--
DROP TABLE IF EXISTS "pages";
CREATE TABLE "pages" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" varchar(32) NOT NULL UNIQUE,
  "verse_count" integer NOT NULL DEFAULT 1,
  "chapter_id" bigint NULL REFERENCES "chapters" ("id") DEFERRABLE INITIALLY DEFERRED,
  "group_id" bigint NULL REFERENCES "groups" ("id") DEFERRABLE INITIALLY DEFERRED,
  "part_id" bigint NULL REFERENCES "parts" ("id") DEFERRABLE INITIALLY DEFERRED,
  "quarter_id" bigint NULL REFERENCES "quarters" ("id") DEFERRABLE INITIALLY DEFERRED
);
DROP INDEX IF EXISTS "pages_verse_count_c0e0d056";
CREATE INDEX "pages_verse_count_c0e0d056" ON "pages" ("verse_count");
DROP INDEX IF EXISTS "pages_chapter_id_a917d251";
CREATE INDEX "pages_chapter_id_a917d251" ON "pages" ("chapter_id");
DROP INDEX IF EXISTS "pages_group_id_43ecf6a9";
CREATE INDEX "pages_group_id_43ecf6a9" ON "pages" ("group_id");
DROP INDEX IF EXISTS "pages_part_id_a8f68ff7";
CREATE INDEX "pages_part_id_a8f68ff7" ON "pages" ("part_id");
DROP INDEX IF EXISTS "pages_quarter_id_48c3ef2b";
CREATE INDEX "pages_quarter_id_48c3ef2b" ON "pages" ("quarter_id");

--
-- Create model Verse
--
DROP TABLE IF EXISTS "verses";
CREATE TABLE "verses" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "number" integer NOT NULL,
  "content" varchar(1024) NOT NULL,
  "chapter_id" bigint NOT NULL REFERENCES "chapters" ("id") DEFERRABLE INITIALLY DEFERRED,
  "group_id" bigint NULL REFERENCES "groups" ("id") DEFERRABLE INITIALLY DEFERRED,
  "page_id" bigint NULL REFERENCES "pages" ("id") DEFERRABLE INITIALLY DEFERRED,
  "part_id" bigint NULL REFERENCES "parts" ("id") DEFERRABLE INITIALLY DEFERRED,
  "quarter_id" bigint NULL REFERENCES "quarters" ("id") DEFERRABLE INITIALLY DEFERRED
);
DROP INDEX IF EXISTS "verses_chapter_id_number_ca67eca3_uniq";
CREATE UNIQUE INDEX "verses_chapter_id_number_ca67eca3_uniq" ON "verses" ("chapter_id", "number");
DROP INDEX IF EXISTS "verses_number_3a23b3b1";
CREATE INDEX "verses_number_3a23b3b1" ON "verses" ("number");
DROP INDEX IF EXISTS "verses_content_16c09417";
CREATE INDEX "verses_content_16c09417" ON "verses" ("content");
DROP INDEX IF EXISTS "verses_chapter_id_b472115e";
CREATE INDEX "verses_chapter_id_b472115e" ON "verses" ("chapter_id");
DROP INDEX IF EXISTS "verses_group_id_bb09b36d";
CREATE INDEX "verses_group_id_bb09b36d" ON "verses" ("group_id");
DROP INDEX IF EXISTS "verses_page_id_932c96e6";
CREATE INDEX "verses_page_id_932c96e6" ON "verses" ("page_id");
DROP INDEX IF EXISTS "verses_part_id_cdcfce14";
CREATE INDEX "verses_part_id_cdcfce14" ON "verses" ("part_id");
DROP INDEX IF EXISTS "verses_quarter_id_3a00848c";
CREATE INDEX "verses_quarter_id_3a00848c" ON "verses" ("quarter_id");
COMMIT;
