--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7 (Debian 11.7-0+deb10u1)
-- Dumped by pg_dump version 12.6 (Ubuntu 12.6-0ubuntu0.20.04.1)

-- Started on 2021-03-26 15:47:09 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 95 (class 2615 OID 649450)
-- Name: gn_synchronomade; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA gn_synchronomade;


--
-- TOC entry 8177 (class 0 OID 0)
-- Dependencies: 95
-- Name: SCHEMA gn_synchronomade; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA gn_synchronomade IS 'schéma contenant les erreurs de synchronisation et permettant une compatibilité temporaire avec les outils mobiles de la V1';


SET default_tablespace = '';

--
-- TOC entry 971 (class 1259 OID 724292)
-- Name: bib_criteres_cf; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.bib_criteres_cf (
    id_critere_cf integer NOT NULL,
    code_critere_cf character varying(3),
    nom_critere_cf character varying(90),
    tri_cf integer,
    cincomplet character(2),
    id_critere_synthese integer
);


--
-- TOC entry 972 (class 1259 OID 724295)
-- Name: bib_criteres_inv; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.bib_criteres_inv (
    id_critere_inv integer NOT NULL,
    code_critere_inv character varying(3),
    nom_critere_inv character varying(90),
    tri_inv integer,
    id_critere_synthese integer
);


--
-- TOC entry 967 (class 1259 OID 724280)
-- Name: bib_messages_cf; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.bib_messages_cf (
    id_message_cf integer NOT NULL,
    texte_message_cf character varying(255)
);


--
-- TOC entry 968 (class 1259 OID 724283)
-- Name: bib_messages_cflore; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.bib_messages_cflore (
    id_message_cflore integer NOT NULL,
    texte_message_cflore character varying(255)
);


--
-- TOC entry 969 (class 1259 OID 724286)
-- Name: bib_messages_inv; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.bib_messages_inv (
    id_message_inv integer NOT NULL,
    texte_message_inv character varying(255)
);


--
-- TOC entry 973 (class 1259 OID 724298)
-- Name: bib_milieux_inv; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.bib_milieux_inv (
    id_milieu_inv integer NOT NULL,
    nom_milieu_inv character varying(50)
);


--
-- TOC entry 970 (class 1259 OID 724289)
-- Name: cor_boolean; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.cor_boolean (
    expression character varying(25) NOT NULL,
    bool boolean
);


--
-- TOC entry 974 (class 1259 OID 724301)
-- Name: cor_critere_liste; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.cor_critere_liste (
    id_critere_cf integer NOT NULL,
    id_liste integer NOT NULL
);


--
-- TOC entry 965 (class 1259 OID 724274)
-- Name: cor_message_taxon_cflore; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.cor_message_taxon_cflore (
    id_message_cflore integer NOT NULL,
    id_nom integer NOT NULL
);


--
-- TOC entry 964 (class 1259 OID 724241)
-- Name: cor_message_taxon_contactfaune; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.cor_message_taxon_contactfaune (
    id_message_cf integer NOT NULL,
    id_nom integer NOT NULL
);


--
-- TOC entry 966 (class 1259 OID 724277)
-- Name: cor_message_taxon_contactinv; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.cor_message_taxon_contactinv (
    id_message_inv integer NOT NULL,
    id_nom integer NOT NULL
);


--
-- TOC entry 727 (class 1259 OID 649453)
-- Name: erreurs_flora; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.erreurs_flora (
    id integer NOT NULL,
    json text,
    date_import date
);


--
-- TOC entry 726 (class 1259 OID 649451)
-- Name: erreurs_flora_id_seq; Type: SEQUENCE; Schema: gn_synchronomade; Owner: -
--

CREATE SEQUENCE gn_synchronomade.erreurs_flora_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 8178 (class 0 OID 0)
-- Dependencies: 726
-- Name: erreurs_flora_id_seq; Type: SEQUENCE OWNED BY; Schema: gn_synchronomade; Owner: -
--

ALTER SEQUENCE gn_synchronomade.erreurs_flora_id_seq OWNED BY gn_synchronomade.erreurs_flora.id;


--
-- TOC entry 729 (class 1259 OID 649462)
-- Name: erreurs_occtax; Type: TABLE; Schema: gn_synchronomade; Owner: -
--

CREATE TABLE gn_synchronomade.erreurs_occtax (
    id integer NOT NULL,
    json text,
    date_import date
);


--
-- TOC entry 728 (class 1259 OID 649460)
-- Name: erreurs_occtax_id_seq; Type: SEQUENCE; Schema: gn_synchronomade; Owner: -
--

CREATE SEQUENCE gn_synchronomade.erreurs_occtax_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 8179 (class 0 OID 0)
-- Dependencies: 728
-- Name: erreurs_occtax_id_seq; Type: SEQUENCE OWNED BY; Schema: gn_synchronomade; Owner: -
--

ALTER SEQUENCE gn_synchronomade.erreurs_occtax_id_seq OWNED BY gn_synchronomade.erreurs_occtax.id;


--
-- TOC entry 1339 (class 1259 OID 988385)
-- Name: v_color_taxon_area; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_color_taxon_area AS
 SELECT bn.id_nom,
    v_area_taxon.id_area,
    v_area_taxon.nb_obs,
    v_area_taxon.last_date,
        CASE
            WHEN (date_part('day'::text, (now() - (v_area_taxon.last_date)::timestamp with time zone)) < (365)::double precision) THEN 'grey'::text
            ELSE 'red'::text
        END AS color
   FROM (gn_synthese.v_area_taxon v_area_taxon
     JOIN taxonomie.bib_noms bn ON ((bn.cd_nom = v_area_taxon.cd_nom)));


--
-- TOC entry 735 (class 1259 OID 649515)
-- Name: v_mobile_recherche; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_mobile_recherche AS
( SELECT ap.indexap AS gid,
    zp.dateobs,
    t.latin AS taxon,
    o.observateurs,
    public.st_asgeojson(public.st_transform(ap.the_geom_local, 4326)) AS geom_4326,
    public.st_x(public.st_transform(public.st_centroid(ap.the_geom_local), 4326)) AS centroid_x,
    public.st_y(public.st_transform(public.st_centroid(ap.the_geom_local), 4326)) AS centroid_y
   FROM (((v1_florepatri.t_apresence ap
     JOIN v1_florepatri.t_zprospection zp ON ((ap.indexzp = zp.indexzp)))
     JOIN v1_florepatri.bib_taxons_fp t ON ((t.cd_nom = zp.cd_nom)))
     JOIN ( SELECT c.indexzp,
            array_to_string(array_agg((((r.prenom_role)::text || ' '::text) || (r.nom_role)::text)), ', '::text) AS observateurs
           FROM (v1_florepatri.cor_zp_obs c
             JOIN utilisateurs.t_roles r ON ((r.id_role = c.codeobs)))
          GROUP BY c.indexzp) o ON ((o.indexzp = ap.indexzp)))
  WHERE ((ap.supprime = false) AND public.st_isvalid(ap.the_geom_local) AND (ap.topo_valid = true))
  ORDER BY zp.dateobs DESC)
UNION
( SELECT cft.id_station AS gid,
    s.dateobs,
    t.latin AS taxon,
    o.observateurs,
    public.st_asgeojson(public.st_transform(s.the_geom_3857, 4326)) AS geom_4326,
    public.st_x(public.st_transform(public.st_centroid(s.the_geom_3857), 4326)) AS centroid_x,
    public.st_y(public.st_transform(public.st_centroid(s.the_geom_3857), 4326)) AS centroid_y
   FROM (((v1_florestation.cor_fs_taxon cft
     JOIN v1_florestation.t_stations_fs s ON ((s.id_station = cft.id_station)))
     JOIN v1_florepatri.bib_taxons_fp t ON ((t.cd_nom = cft.cd_nom)))
     JOIN ( SELECT c.id_station,
            array_to_string(array_agg((((r.prenom_role)::text || ' '::text) || (r.nom_role)::text)), ', '::text) AS observateurs
           FROM (v1_florestation.cor_fs_observateur c
             JOIN utilisateurs.t_roles r ON ((r.id_role = c.id_role)))
          GROUP BY c.id_station) o ON ((o.id_station = cft.id_station)))
  WHERE ((cft.supprime = false) AND public.st_isvalid(s.the_geom_3857))
  ORDER BY s.dateobs DESC);


--
-- TOC entry 1062 (class 1259 OID 971705)
-- Name: v_nomade_classes; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_classes AS
 SELECT g.id_liste AS id_classe,
    g.nom_liste AS nom_classe_fr,
    g.desc_liste AS desc_classe
   FROM (( SELECT l.id_liste,
            l.nom_liste,
            l.desc_liste,
            min(taxonomie.find_cdref(n.cd_nom)) AS cd_ref
           FROM ((taxonomie.bib_listes l
             JOIN taxonomie.cor_nom_liste cnl ON ((cnl.id_liste = l.id_liste)))
             JOIN taxonomie.bib_noms n ON ((n.id_nom = cnl.id_nom)))
          WHERE (l.id_liste = ANY (ARRAY[1, 11, 12, 13, 14]))
          GROUP BY l.id_liste, l.nom_liste, l.desc_liste) g
     JOIN taxonomie.taxref t ON ((t.cd_nom = g.cd_ref)))
  WHERE ((t.phylum)::text = 'Chordata'::text);


--
-- TOC entry 732 (class 1259 OID 649503)
-- Name: v_nomade_criteres_cf; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_criteres_cf AS
 SELECT c.id_critere_cf,
    c.nom_critere_cf,
    c.tri_cf,
    ccl.id_liste AS id_classe
   FROM (gn_synchronomade.bib_criteres_cf c
     JOIN gn_synchronomade.cor_critere_liste ccl ON ((ccl.id_critere_cf = c.id_critere_cf)))
  ORDER BY ccl.id_liste, c.tri_cf;


--
-- TOC entry 733 (class 1259 OID 649507)
-- Name: v_nomade_criteres_inv; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_criteres_inv AS
 SELECT c.id_critere_inv,
    c.nom_critere_inv,
    c.tri_inv
   FROM gn_synchronomade.bib_criteres_inv c
  ORDER BY c.tri_inv;


--
-- TOC entry 734 (class 1259 OID 649511)
-- Name: v_nomade_milieux_inv; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_milieux_inv AS
 SELECT v1.id_milieu_inv,
    v1.nom_milieu_inv
   FROM hist_contactinv.bib_milieux_inv v1
  ORDER BY v1.id_milieu_inv;


--
-- TOC entry 731 (class 1259 OID 649498)
-- Name: v_nomade_observateurs_faune; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_observateurs_faune AS
 SELECT DISTINCT r.id_role,
    r.nom_role,
    r.prenom_role
   FROM utilisateurs.t_roles r
  WHERE ((r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
           FROM utilisateurs.cor_roles cr
          WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
                   FROM utilisateurs.cor_role_menu crm
                  WHERE (crm.id_menu = 11)))
          ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
           FROM (utilisateurs.cor_role_menu crm
             JOIN utilisateurs.t_roles r_1 ON (((r_1.id_role = crm.id_role) AND (crm.id_menu = 11) AND (r_1.groupe = false) AND (r_1.active = true)))))))
  ORDER BY r.nom_role, r.prenom_role, r.id_role;


--
-- TOC entry 730 (class 1259 OID 649493)
-- Name: v_nomade_observateurs_inv; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_observateurs_inv AS
 SELECT DISTINCT r.id_role,
    r.nom_role,
    r.prenom_role
   FROM utilisateurs.t_roles r
  WHERE ((r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
           FROM utilisateurs.cor_roles cr
          WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
                   FROM utilisateurs.cor_role_menu crm
                  WHERE (crm.id_menu = 11)))
          ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
           FROM (utilisateurs.cor_role_menu crm
             JOIN utilisateurs.t_roles r_1 ON (((r_1.id_role = crm.id_role) AND (crm.id_menu = 11) AND (r_1.groupe = false) AND (r_1.active = true)))))))
  ORDER BY r.nom_role, r.prenom_role, r.id_role;


--
-- TOC entry 1061 (class 1259 OID 971700)
-- Name: v_nomade_taxons_faune; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_taxons_faune AS
 SELECT DISTINCT n.id_nom,
    taxonomie.find_cdref(n.cd_nom) AS cd_ref,
    n.cd_nom,
    tx.lb_nom AS nom_latin,
    n.nom_francais,
    cnl.id_liste AS id_classe,
        CASE
            WHEN (tx.cd_nom = ANY (ARRAY[61098, 61119, 61000])) THEN 6
            ELSE 5
        END AS denombrement,
    f2.bool AS patrimonial,
    m.texte_message_cf AS message,
        CASE
            WHEN (tx.cd_nom = ANY (ARRAY[60577, 60612])) THEN false
            ELSE true
        END AS contactfaune,
    true AS mortalite
   FROM (((((((taxonomie.bib_noms n
     LEFT JOIN gn_synchronomade.cor_message_taxon_contactfaune cmt ON ((cmt.id_nom = n.id_nom)))
     LEFT JOIN gn_synchronomade.bib_messages_cf m ON ((m.id_message_cf = cmt.id_message_cf)))
     LEFT JOIN taxonomie.cor_taxon_attribut cta ON ((cta.cd_ref = n.cd_ref)))
     JOIN taxonomie.cor_nom_liste cnl ON (((cnl.id_nom = n.id_nom) AND (cnl.id_liste = ANY (ARRAY[1, 11, 12, 13, 14])))))
     JOIN taxonomie.cor_nom_liste cnl_500 ON (((cnl_500.id_nom = n.id_nom) AND (cnl_500.id_liste = 500))))
     JOIN taxonomie.taxref tx ON (((tx.cd_nom = n.cd_nom) AND ((tx.phylum)::text = 'Chordata'::text))))
     JOIN gn_synchronomade.cor_boolean f2 ON ((((f2.expression)::text = cta.valeur_attribut) AND (cta.id_attribut = 1))))
  ORDER BY n.id_nom, (taxonomie.find_cdref(n.cd_nom)), tx.lb_nom, n.nom_francais, cnl.id_liste, f2.bool, m.texte_message_cf;


--
-- TOC entry 1060 (class 1259 OID 971695)
-- Name: v_nomade_taxons_flore; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_taxons_flore AS
 SELECT DISTINCT n.id_nom,
    taxonomie.find_cdref(n.cd_nom) AS cd_ref,
    n.cd_nom,
    tx.lb_nom AS nom_latin,
    n.nom_francais,
    cnl.id_liste AS id_classe,
        CASE
            WHEN (tx.cd_nom = ANY (ARRAY[61098, 61119, 61000])) THEN 6
            ELSE 5
        END AS denombrement,
    f2.bool AS patrimonial,
    m.texte_message_cflore AS message,
        CASE
            WHEN (tx.cd_nom = ANY (ARRAY[60577, 60612])) THEN false
            ELSE true
        END AS contactfaune,
    true AS mortalite
   FROM (((((((taxonomie.bib_noms n
     LEFT JOIN gn_synchronomade.cor_message_taxon_cflore cmt ON ((cmt.id_nom = n.id_nom)))
     LEFT JOIN gn_synchronomade.bib_messages_cflore m ON ((m.id_message_cflore = cmt.id_message_cflore)))
     LEFT JOIN taxonomie.cor_taxon_attribut cta ON ((cta.cd_ref = n.cd_ref)))
     JOIN taxonomie.cor_nom_liste cnl ON (((cnl.id_nom = n.id_nom) AND (cnl.id_liste > 300) AND (cnl.id_liste < 400))))
     JOIN taxonomie.cor_nom_liste cnl_500 ON (((cnl_500.id_nom = n.id_nom) AND (cnl_500.id_liste = 500))))
     JOIN taxonomie.taxref tx ON (((tx.cd_nom = n.cd_nom) AND ((tx.regne)::text = 'Plantae'::text))))
     JOIN gn_synchronomade.cor_boolean f2 ON ((((f2.expression)::text = cta.valeur_attribut) AND (cta.id_attribut = 1))))
  ORDER BY n.id_nom, (taxonomie.find_cdref(n.cd_nom)), tx.lb_nom, n.nom_francais, cnl.id_liste, f2.bool, m.texte_message_cflore;


--
-- TOC entry 1059 (class 1259 OID 971690)
-- Name: v_nomade_taxons_inv; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_taxons_inv AS
 SELECT DISTINCT n.id_nom,
    taxonomie.find_cdref(n.cd_nom) AS cd_ref,
    n.cd_nom,
    tx.lb_nom AS nom_latin,
    n.nom_francais,
    cnl.id_liste AS id_classe,
        CASE
            WHEN (tx.cd_nom = ANY (ARRAY[61098, 61119, 61000])) THEN 6
            ELSE 5
        END AS denombrement,
    f2.bool AS patrimonial,
    m.texte_message_inv AS message,
        CASE
            WHEN (tx.cd_nom = ANY (ARRAY[60577, 60612])) THEN false
            ELSE true
        END AS contactfaune,
    true AS mortalite
   FROM (((((((taxonomie.bib_noms n
     LEFT JOIN gn_synchronomade.cor_message_taxon_contactinv cmt ON ((cmt.id_nom = n.id_nom)))
     LEFT JOIN gn_synchronomade.bib_messages_inv m ON ((m.id_message_inv = cmt.id_message_inv)))
     LEFT JOIN taxonomie.cor_taxon_attribut cta ON ((cta.cd_ref = n.cd_ref)))
     JOIN taxonomie.cor_nom_liste cnl ON (((cnl.id_nom = n.id_nom) AND (cnl.id_liste = ANY (ARRAY[2, 5, 8, 9, 10, 15, 16])))))
     JOIN taxonomie.cor_nom_liste cnl_500 ON (((cnl_500.id_nom = n.id_nom) AND (cnl_500.id_liste = 500))))
     JOIN taxonomie.taxref tx ON ((tx.cd_nom = n.cd_nom)))
     JOIN gn_synchronomade.cor_boolean f2 ON ((((f2.expression)::text = cta.valeur_attribut) AND (cta.id_attribut = 1))))
  ORDER BY n.id_nom, (taxonomie.find_cdref(n.cd_nom)), tx.lb_nom, n.nom_francais, cnl.id_liste, f2.bool, m.texte_message_inv;


--
-- TOC entry 997 (class 1259 OID 770219)
-- Name: v_nomade_unites_geo_inv; Type: VIEW; Schema: gn_synchronomade; Owner: -
--

CREATE VIEW gn_synchronomade.v_nomade_unites_geo_inv AS
 SELECT public.st_simplifypreservetopology(l_areas.geom, (15)::double precision) AS the_geom,
    l_areas.id_area AS id_unite_geo
   FROM ref_geo.l_areas
  WHERE (l_areas.id_type = 24)
  GROUP BY l_areas.id_area;


--
-- TOC entry 7890 (class 2604 OID 649456)
-- Name: erreurs_flora id; Type: DEFAULT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.erreurs_flora ALTER COLUMN id SET DEFAULT nextval('gn_synchronomade.erreurs_flora_id_seq'::regclass);


--
-- TOC entry 7891 (class 2604 OID 649465)
-- Name: erreurs_occtax id; Type: DEFAULT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.erreurs_occtax ALTER COLUMN id SET DEFAULT nextval('gn_synchronomade.erreurs_occtax_id_seq'::regclass);


--
-- TOC entry 7911 (class 2606 OID 724376)
-- Name: bib_criteres_cf bib_criteres_cf_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.bib_criteres_cf
    ADD CONSTRAINT bib_criteres_cf_pkey PRIMARY KEY (id_critere_cf);


--
-- TOC entry 7913 (class 2606 OID 724378)
-- Name: bib_criteres_inv bib_criteres_inv_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.bib_criteres_inv
    ADD CONSTRAINT bib_criteres_inv_pkey PRIMARY KEY (id_critere_inv);


--
-- TOC entry 7903 (class 2606 OID 724380)
-- Name: bib_messages_cf bib_messages_cf_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.bib_messages_cf
    ADD CONSTRAINT bib_messages_cf_pkey PRIMARY KEY (id_message_cf);


--
-- TOC entry 7905 (class 2606 OID 724384)
-- Name: bib_messages_cflore bib_messages_cflore_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.bib_messages_cflore
    ADD CONSTRAINT bib_messages_cflore_pkey PRIMARY KEY (id_message_cflore);


--
-- TOC entry 7907 (class 2606 OID 724382)
-- Name: bib_messages_inv bib_messages_inv_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.bib_messages_inv
    ADD CONSTRAINT bib_messages_inv_pkey PRIMARY KEY (id_message_inv);


--
-- TOC entry 7915 (class 2606 OID 724386)
-- Name: bib_milieux_inv bib_milieux_inv_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.bib_milieux_inv
    ADD CONSTRAINT bib_milieux_inv_pkey PRIMARY KEY (id_milieu_inv);


--
-- TOC entry 7909 (class 2606 OID 724374)
-- Name: cor_boolean cor_boolean_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_boolean
    ADD CONSTRAINT cor_boolean_pkey PRIMARY KEY (expression);


--
-- TOC entry 7917 (class 2606 OID 724394)
-- Name: cor_critere_liste cor_cor_critere_liste_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_critere_liste
    ADD CONSTRAINT cor_cor_critere_liste_pkey PRIMARY KEY (id_critere_cf, id_liste);


--
-- TOC entry 7899 (class 2606 OID 724392)
-- Name: cor_message_taxon_cflore cor_message_taxon_cflore_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_cflore
    ADD CONSTRAINT cor_message_taxon_cflore_pkey PRIMARY KEY (id_message_cflore, id_nom);


--
-- TOC entry 7897 (class 2606 OID 724388)
-- Name: cor_message_taxon_contactfaune cor_message_taxon_contactfaune_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_contactfaune
    ADD CONSTRAINT cor_message_taxon_contactfaune_pkey PRIMARY KEY (id_message_cf, id_nom);


--
-- TOC entry 7901 (class 2606 OID 724390)
-- Name: cor_message_taxon_contactinv cor_message_taxon_contactinv_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_contactinv
    ADD CONSTRAINT cor_message_taxon_contactinv_pkey PRIMARY KEY (id_message_inv, id_nom);


--
-- TOC entry 7893 (class 2606 OID 649470)
-- Name: erreurs_flora erreurs_flora_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.erreurs_flora
    ADD CONSTRAINT erreurs_flora_pkey PRIMARY KEY (id);


--
-- TOC entry 7895 (class 2606 OID 649472)
-- Name: erreurs_occtax erreurs_occtax_pkey; Type: CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.erreurs_occtax
    ADD CONSTRAINT erreurs_occtax_pkey PRIMARY KEY (id);


--
-- TOC entry 7924 (class 2606 OID 724435)
-- Name: cor_critere_liste fk_cor_critere_liste_bib_criter; Type: FK CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_critere_liste
    ADD CONSTRAINT fk_cor_critere_liste_bib_criter FOREIGN KEY (id_critere_cf) REFERENCES gn_synchronomade.bib_criteres_cf(id_critere_cf) ON UPDATE CASCADE;


--
-- TOC entry 7925 (class 2606 OID 724440)
-- Name: cor_critere_liste fk_cor_critere_liste_bib_liste; Type: FK CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_critere_liste
    ADD CONSTRAINT fk_cor_critere_liste_bib_liste FOREIGN KEY (id_liste) REFERENCES taxonomie.bib_listes(id_liste) ON UPDATE CASCADE;


--
-- TOC entry 7918 (class 2606 OID 724450)
-- Name: cor_message_taxon_contactfaune fk_cor_message_taxoncf_bib_message_cf; Type: FK CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_contactfaune
    ADD CONSTRAINT fk_cor_message_taxoncf_bib_message_cf FOREIGN KEY (id_message_cf) REFERENCES gn_synchronomade.bib_messages_cf(id_message_cf) ON UPDATE CASCADE;


--
-- TOC entry 7919 (class 2606 OID 724445)
-- Name: cor_message_taxon_contactfaune fk_cor_message_taxoncf_bib_noms_fa; Type: FK CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_contactfaune
    ADD CONSTRAINT fk_cor_message_taxoncf_bib_noms_fa FOREIGN KEY (id_nom) REFERENCES taxonomie.bib_noms(id_nom) ON UPDATE CASCADE;


--
-- TOC entry 7920 (class 2606 OID 724470)
-- Name: cor_message_taxon_cflore fk_cor_message_taxoncflore_bib_message_cflore; Type: FK CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_cflore
    ADD CONSTRAINT fk_cor_message_taxoncflore_bib_message_cflore FOREIGN KEY (id_message_cflore) REFERENCES gn_synchronomade.bib_messages_cflore(id_message_cflore) ON UPDATE CASCADE;


--
-- TOC entry 7921 (class 2606 OID 724465)
-- Name: cor_message_taxon_cflore fk_cor_message_taxoncflore_bib_noms; Type: FK CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_cflore
    ADD CONSTRAINT fk_cor_message_taxoncflore_bib_noms FOREIGN KEY (id_nom) REFERENCES taxonomie.bib_noms(id_nom) ON UPDATE CASCADE;


--
-- TOC entry 7922 (class 2606 OID 724460)
-- Name: cor_message_taxon_contactinv fk_cor_message_taxoninv_bib_message_inv; Type: FK CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_contactinv
    ADD CONSTRAINT fk_cor_message_taxoninv_bib_message_inv FOREIGN KEY (id_message_inv) REFERENCES gn_synchronomade.bib_messages_inv(id_message_inv) ON UPDATE CASCADE;


--
-- TOC entry 7923 (class 2606 OID 724455)
-- Name: cor_message_taxon_contactinv fk_cor_message_taxoninv_bib_noms; Type: FK CONSTRAINT; Schema: gn_synchronomade; Owner: -
--

ALTER TABLE ONLY gn_synchronomade.cor_message_taxon_contactinv
    ADD CONSTRAINT fk_cor_message_taxoninv_bib_noms FOREIGN KEY (id_nom) REFERENCES taxonomie.bib_noms(id_nom) ON UPDATE CASCADE;


-- Completed on 2021-03-26 15:47:28 CET

--
-- PostgreSQL database dump complete
--

