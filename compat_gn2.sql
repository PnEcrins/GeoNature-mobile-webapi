CREATE SCHEMA synchronomade;

CREATE TABLE synchronomade.erreurs_occtax
(
  id serial NOT NULL,
  json text,
  date_import date,
  CONSTRAINT erreurs_occtax_pkey PRIMARY KEY (id)
)



-- debug develop

--  DELETE FROM pr_occtax.t_releves_occtax WHERE id_releve_occtax=424789324;
--  DELETE FROM pr_occtax.t_occurrences_occtax WHERE id_occurrence_occtax=424789419;
--  DELETE FROM pr_occtax.t_occurrences_occtax WHERE id_occurrence_occtax=424789469;
-- DELETE FROM pr_occtax.t_occurrences_occtax WHERE id_occurrence_occtax=424789507;
-- DELETE FROM pr_occtax.t_occurrences_occtax WHERE id_occurrence_occtax=424789545;
-- DELETE FROM pr_occtax.t_occurrences_occtax WHERE id_occurrence_occtax=605204510;

-- SELECT pg_catalog.setval('pr_occtax.t_occurrences_occtax_id_occurrence_occtax_seq', SELECT max(id_occurrence_occtax) FROM pr_occtax.t_occurrences_occtax, true);



-- json à poster

{
	"token": 666,
	"data": {
	"input_type":"fauna","id":424789324,"dateobs":"2013\/06\/17","geolocation":{"accuracy":0,"longitude":6.058308195425622,"latitude":44.92673320582596},"taxons":[{"id_taxon":3,"id":424789419,"name_entered":"Accenteur alpin","observation":{"criterion":5},"counting":{"yearling":0,"adult_female":0,"not_adult":0,"adult":0,"sex_age_unspecified":0,"young":0,"adult_male":1},"comment":""},{"id_taxon":1,"id":424789469,"name_entered":"Pipit spioncelle","observation":{"criterion":7},"counting":{"yearling":0,"adult_female":0,"not_adult":0,"adult":0,"sex_age_unspecified":0,"young":0,"adult_male":2},"comment":""},{"id_taxon":2,"id":424789507,"name_entered":"Rougequeue noir","observation":{"criterion":5},"counting":{"yearling":0,"adult_female":0,"not_adult":0,"adult":0,"sex_age_unspecified":0,"young":0,"adult_male":1},"comment":""},{"id_taxon":4,"id":424789545,"name_entered":"Traquet motteux","observation":{"criterion":5},"counting":{"yearling":0,"adult_female":0,"not_adult":0,"adult":0,"sex_age_unspecified":0,"young":0,"adult_male":2},"comment":""}],"initial_input":"pda","observers_id":[223]
	
	}
}