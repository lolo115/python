drop table emp purge;
create table emp as select first_name, last_name, salary from hr.employees;


CREATE OR REPLACE PROCEDURE GENERAL_SAL_INCREASE (pct in number default 0) is
begin
if (pct > 100 or pct<0) then
  raise_application_error(-20000,'pct must be set between 0 and 100');
end if;
update emp set salary=salary*(1+(pct/100));
commit;
end;
/

CREATE OR REPLACE PROCEDURE GENERAL_SAL_INCREASE_OUT (pct in number default 0, avg_sal out number) is
begin
if (pct > 100 or pct<0) then
  raise_application_error(-20000,'pct must be set between 0 and 100');
end if;

update emp set salary=salary*(1+(pct/100));
commit;

select avg(salary) into avg_sal from emp;

end;
/

CREATE OR REPLACE EDITIONABLE FUNCTION "LAURENT"."GET_SAL" (fname in varchar2, lname in varchar2) return number
is
 sal number;
 l_ln varchar2(128) := lower(lname);
 l_fn varchar2(128) := lower(fname);
begin
 select salary into sal from emp where lower(first_name) like '%'||l_fn||'%' and lower(last_name) like '%'||l_ln||'%';
 return sal;
exception
   when NO_DATA_FOUND then raise_application_error(-20000,'No employee with this last_name and first_name');
end;
/

