DROP
  VIEW IF EXISTS "al-quran";
CREATE VIEW "al-quran" AS 
SELECT 
  "verses"."id", 
  "number", 
  "content", 
  "chapter_id" AS "chapter", 
  "name", 
  "order", 
  "type", 
  "verse_count", 
  "part_id" AS "part", 
  "group_id" AS "group", 
  "quarter_id" AS "quarter", 
  "page_id" AS "page" 
FROM 
  "verses" 
  join "chapters" ON "verses"."chapter_id" = "chapters"."id";
