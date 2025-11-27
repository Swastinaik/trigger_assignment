-- app/sql/triggers.sql
CREATE OR REPLACE FUNCTION fn_inc_member_checkins()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE "member" SET total_check_ins = total_check_ins + 1 WHERE id = NEW.member_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_attendance_after_insert ON attendance;

CREATE TRIGGER trg_attendance_after_insert
AFTER INSERT ON attendance
FOR EACH ROW
EXECUTE FUNCTION fn_inc_member_checkins();
