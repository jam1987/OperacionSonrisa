drop trigger t_calcula_edad on persona;
create or replace function calcula_edad()
	returns trigger
	language plpgsql
	as
$$
DECLARE
fechaact DATE;
BEGIN
	SELECT CURRENT_DATE into fechaact;
	new.edad:=FLOOR(((DATE_PART('YEAR',fechaact)-DATE_PART('YEAR',new.fechanac))* 372 + (DATE_PART('MONTH',fechaact) - DATE_PART('MONTH',new.fechanac))*31 + (DATE_PART('DAY',fechaact)-DATE_PART('DAY',new.fechanac)))/372);
	return new;
END
$$;

create trigger t_calcula_edad
	before insert on persona
	for each row
	execute procedure calcula_edad();