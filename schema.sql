CREATE DOMAIN truck_type AS text CHECK (
    VALUE = 'Engine' OR
    VALUE = 'Ladder' OR
    VALUE = 'Medic' OR
    VALUE = 'Heavy Rescue'
);

CREATE DOMAIN incident_class AS text CHECK (
    VALUE = 'Fire' OR
    VALUE = 'Medical' OR
    VALUE = 'Hazmat' OR
    VALUE = 'Electrical' OR
    VALUE = 'Accident'
);

CREATE DOMAIN incident_subclass AS text CHECK (
    VALUE = 'Dwelling' OR
    VALUE = 'High-Rise' OR
    VALUE = 'Car'
);

CREATE DOMAIN status_type AS text CHECK (
    VALUE = 'Active' OR
    VALUE = 'Inactive' OR
    VALUE = 'Decommissioned' OR
    VALUE = 'Maintenance'
);

CREATE TABLE stations (
    id UUID PRIMARY KEY,
    battalion smallint NOT NULL,
    location point NOT NULL,
    status status_type DEFAULT 'Active'::text,
    neighborhood text NOT NULL,
    address text NOT NULL,
    city text DEFAULT 'Philadelphia'::text NOT NULL,
    state text DEFAULT 'PA'::text NOT NULL,
    postal_code text,
    phone smallint,
    radio_band text,
    chief text,
    service_area path,
    last_modified timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE trucks (
    id UUID PRIMARY KEY,
    station_id UUID NOT NULL references stations(id),
    type truck_type DEFAULT 'Engine'::text,
    status status_type DEFAULT 'Active'::text,
    description text
);

CREATE TABLE incidents (
    id UUID PRIMARY KEY,
    duration tstzrange NOT NULL,
    classification incident_class NOT NULL,
    subclassification incident_subclass NOT NULL,
    alarm integer DEFAULT 1::integer,
    location Point NOT NULL,
    description text
);

CREATE TABLE incident_responders (
    incident_id UUID PRIMARY KEY references incidents(id),
    station_id UUID NOT NULL references stations(id),
    truck_id UUID NOT NULL references trucks(id),
    arrived_at timestamptz,
    dispatched_at timestamptz
);

CREATE TABLE truck_runs (
    station_id UUID NOT NULL,
    truck_id UUID NOT NULL,
    year smallint NOT NULL,
    runs integer DEFAULT 0::integer NOT NULL
);

CREATE TABLE station_runs (
    station_id UUID NOT NULL,
    year smallint NOT NULL,
    runs integer DEFAULT 0::integer NOT NULL
);

CREATE INDEX incident_duration_idx on incidents USING gist(duration);

CREATE OR REPLACE FUNCTION public.get_incidents_by_timerange(in_range tstzrange)
  RETURNS public.incidents
  LANGUAGE SQL
  STRICT
  SECURITY DEFINER
  SET SEARCH_PATH TO public, pg_temp
  AS
$$
    SELECT *
      FROM public.incidents
     WHERE duration && $1;
$$;

CREATE OR REPLACE FUNCTION public.get_stations()
  RETURNS public.stations
  LANGUAGE SQL
  STRICT
  SECURITY DEFINER
  SET SEARCH_PATH TO public, pg_temp
  AS
$$
    SELECT *
      FROM public.stations;
$$;

CREATE OR REPLACE FUNCTION public.get_trucks()
  RETURNS public.trucks
  LANGUAGE SQL
  STRICT
  SECURITY DEFINER
  SET SEARCH_PATH TO public, pg_temp
  AS
$$
    SELECT *
      FROM public.trucks;
$$;

