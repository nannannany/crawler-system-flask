CREATE TABLE public.base_crawlers (
    id integer NOT NULL,
    switch_status integer DEFAULT 0 NOT NULL,
    frequency integer DEFAULT 1 NOT NULL,
    crawler_status integer DEFAULT 0 NOT NULL,
    last_run_time timestamp without time zone,
    next_run_time timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE public.crawl_pool (
    id integer NOT NULL,
    source_url character varying(500),
    keyword character varying(100) NOT NULL,
    config_names jsonb DEFAULT '[]'::json NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    website_names character varying(255),
    category character varying(50) DEFAULT ''::character varying NOT NULL
);

CREATE TABLE public.crawl_results (
    id integer NOT NULL,
    category character varying(50) NOT NULL,
    keyword character varying(100) NOT NULL,
    website_name character varying(100) NOT NULL,
    source_url character varying(500) NOT NULL,
    title character varying(500) NOT NULL,
    detail_url character varying(500) NOT NULL,
    publish_time timestamp without time zone,
    publisher character varying(200),
    is_pushed integer DEFAULT 0 NOT NULL,
    crawled_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    config_name character varying(100)
);

CREATE TABLE public.crawler_configs (
    config_name character varying(100) NOT NULL,
    keywords json DEFAULT '[]'::json NOT NULL,
    website_names json DEFAULT '[]'::json NOT NULL,
    source_urls json DEFAULT '[]'::json NOT NULL,
    category character varying(50) NOT NULL,
    created_user character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE public.heartbeat (
    id integer NOT NULL,
    caiji_heartbeat timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    caiji_status smallint DEFAULT 0 NOT NULL,
    email_heartbeat timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    email_status smallint DEFAULT 0 NOT NULL
);

CREATE TABLE public.users (
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    push_categories json DEFAULT '[]'::json NOT NULL,
    push_switch integer DEFAULT 1 NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);