CREATE TABLE maintenancezone.maintanence_rec (
            maint_id SERIAL PRIMARY KEY,
            maint_actual_start TIMESTAMP,
            maint_actual_end TIMESTAMP,
            maint_schedule_start TIMESTAMP,
            maint_schedule_end TIMESTAMP,
            reason VARCHAR(180),
            vendor VARCHAR(80),
            description VARCHAR(250),
            Assignee VARCHAR(80),
            status VARCHAR(40),
            equipment_location VARCHAR(80),
            priority VARCHAR(12)
        );
