
print("Loading modules...")
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import imlsconfig
print("Building DB classes...")
Base = automap_base()
engine = create_engine(imlsconfig.connectstring)
Base.prepare(engine, reflect=True)
Nodes = Base.classes.node
LRUrls =Base.classes.field_data_field_lr_url
Payment=Base.classes.field_data_field_lr_payment_required
Submitter=Base.classes.field_data_field_dmt_submitter_name
SubmitterEmail=Base.classes.field_data_field_submission_contact_email_a
Authorid=Base.classes.field_data_field_lr_author_people
PeopleFirst=Base.classes.field_data_field_lr_ppl_name_first
PeopleLast=Base.classes.field_data_field_lr_ppl_name_last
AuthorOrg=Base.classes.field_revision_field_lr_author_organizations
TaxonomyTerms=Base.classes.taxonomy_term_data
LongName=Base.classes.field_data_field_long_name
Contact=Base.classes.field_data_field_lr_contact_people
ContactAuthorOrg=Base.classes.field_revision_field_lr_contact_organizations
ContributorPeople= Base.classes.field_revision_field_lr_contributor_people
ContributorPerson=Base.classes.field_data_field_lr_contributor_person
ContributorType=Base.classes.field_revision_field_lr_contributor_type
ContribOrgs=Base.classes.field_revision_field_lr_contributor_orgs
ContribOrg=Base.classes.field_revision_field_lr_contributor_org
Abstracts=Base.classes.field_data_field_lr_abstract
Subjects=Base.classes.field_data_field_lr_subject
Keywords=Base.classes.field_data_field_lr_keywords
Licenses=Base.classes.field_data_field_lr_license
UsageRights=Base.classes.field_data_field_lr_usage_rights
Citation=Base.classes.field_data_field_lr_citation
Locator=Base.classes.field_data_field_lr_locator_id
LocatorType=Base.classes.field_data_field_lr_locator_type
Publisher=Base.classes.field_data_field_lr_publisher
Version=Base.classes.field_data_field_lr_version
DateCreated =Base.classes.field_data_field_lr_date_created
DatePublished =Base.classes.field_data_field_lr_date_published
AccessFeatures =Base.classes.field_data_field_lr_access_features
LanguagePrimary = Base.classes.field_data_field_lr_language_primary
LanguagesSecondary=Base.classes.field_data_field_lr_languages_secondary
print("Creating db session...")
session = Session(engine)



def get_names(id):
    return_object={"lastname": "","firstname": ""}
    firstnamez=session.query(PeopleFirst.field_lr_ppl_name_first_value).filter(PeopleFirst.entity_id==id).first()
    if firstnamez is not None:
        return_object['firstname']=firstnamez[0]
    lastnamez=session.query(PeopleLast.field_lr_ppl_name_last_value).filter(PeopleLast.entity_id==id).first()
    if lastnamez is not None:
        return_object['lastname']=lastnamez[0]
    return return_object


def get_taxonomy_value(id):
        namedata=session.query(TaxonomyTerms.name).filter(TaxonomyTerms.tid==id).first()
        if namedata is not None:
            return namedata[0]
        else:
            return ""

def get_value(field,table):
    value=session.query(field).filter(table.entity_id==lr.nid).first()
    if value is not None:
        return value[0]
    else:
        return ""


def get_date(field,table):
    value=session.query(field).filter(table.entity_id==lr.nid).first()
    if value is not None:
        return value[0].strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        return ""


def get_values(field,table):
    returnarray=[]
    values=session.query(field).filter(table.entity_id==lr.nid).all()
    if values is not None:
        for value in values:
            returnarray.append(value[0])
    return returnarray


def get_name_from_target(field,table):
    id=session.query(field).filter(table.entity_id==lr.nid).first()
    if id is not None:
        return get_names(id[0])
    else:
        return {"lastname": "","firstname": ""}


def get_value_from_target(field,table):
    id=session.query(field).filter(table.entity_id==lr.nid).first()
    if id is not None:
        return get_taxonomy_value(id[0])
    else:
        return ""


def get_values_from_target(field,table):
    ids=session.query(field).filter(table.entity_id==lr.nid).all()
    returnarray=[]
    if ids is not None:
        for id in ids:
            returnarray.append(get_taxonomy_value(id[0]))
    return returnarray


print("Fetching all learning resources...")
Learning_Resources=session.query(Nodes.title,Nodes.nid).filter(Nodes.type=='dmt_learning_resource').all()
jsondict=json.loads('{ "learning_resources":[]}')
for lr in Learning_Resources:

    j=json.loads('{}')
    j['title']=lr.title
    j['url']=get_value(LRUrls.field_lr_url_url,LRUrls)
    j['access_cost']=get_value(Payment.field_lr_payment_required_value,Payment)
    j['submitter_name']=get_value(Submitter.field_dmt_submitter_name_value,Submitter)
    j['submitter_email']=get_value(SubmitterEmail.field_submission_contact_email_a_email,SubmitterEmail)
    j['author']=get_name_from_target(Authorid.field_lr_author_people_target_id,Authorid)
    j['author_org']=get_value_from_target(AuthorOrg.field_lr_author_organizations_target_id,AuthorOrg)
    j['contact']=get_value_from_target(Contact.field_lr_contact_people_target_id,Contact)
    j['contact_org']=get_value_from_target(ContactAuthorOrg.field_lr_contact_organizations_target_id,ContactAuthorOrg)
    j['abstract']={'data':get_value(Abstracts.field_lr_abstract_value,Abstracts),'format':get_value(Abstracts.field_lr_abstract_format,Abstracts)}
    j['subject']=get_value_from_target(Subjects.field_lr_subject_target_id,Subjects)
    j['keywords']=get_values_from_target(Keywords.field_lr_keywords_target_id,Keywords)
    j['licence']=get_value_from_target(Licenses.field_lr_license_target_id,Licenses)
    j['usage_rights']=get_value_from_target(UsageRights.field_lr_usage_rights_target_id,UsageRights)
    j['citation']={'data':get_value(Citation.field_lr_citation_value,Citation),'format':get_value(Citation.field_lr_citation_format,Citation)}
    j['locator']={'data':get_value(Locator.field_lr_locator_id_value,Locator),'type':get_value_from_target(LocatorType.field_lr_locator_type_target_id,LocatorType)}
    j['publisher']=get_value_from_target(Publisher.field_lr_publisher_target_id,Publisher)
    j['version']=get_value(Version.field_lr_version_value,Version)
    j['created']=get_date(DateCreated.field_lr_date_created_value,DateCreated)
    j['published']=get_date(DatePublished.field_lr_date_published_value,DatePublished)
    j['access_features']=get_value_from_target(AccessFeatures.field_lr_access_features_target_id,AccessFeatures)
    j['language_primary']=get_value(LanguagePrimary.field_lr_language_primary_value,LanguagePrimary)
    j['languages_secondary']=get_values(LanguagesSecondary.field_lr_languages_secondary_value,LanguagesSecondary)


    
    # These are ugly, I will refactor later:
    contributors=[]
    for contributorid in get_values(ContributorPeople.field_lr_contributor_people_value,ContributorPeople):
            contributorpersonid=session.query(ContributorPerson.field_lr_contributor_person_target_id).filter(ContributorPerson.entity_id==contributorid).first()
            if contributorpersonid is not None:
                contributorsnames=get_names(contributorpersonid[0])
            contributortype=""
            contributortypeid=session.query(ContributorType.field_lr_contributor_type_target_id).filter(ContributorType.entity_id==contributorid).first()
            if contributortypeid is not None:
                contributortype=get_taxonomy_value(contributortypeid[0])
            contributorsnames.update({'type':contributortype})
            contributors.append(contributorsnames)
    j['contributors']=contributors
    contributororgsvals=session.query(ContribOrgs.field_lr_contributor_orgs_value).filter(ContribOrgs.entity_id==lr.nid).all()
    contributororgs=[]
    if contributororgsvals is not None:
        contributortype=""
        for contributororgsval in contributororgsvals:
            contributororg=""
            contributortype=""
            contributorpersonid=session.query(ContribOrg.field_lr_contributor_org_target_id).filter(ContribOrg.entity_id==contributororgsval[0]).first()
            if contributorpersonid is not None:
                contributororg=get_taxonomy_value(contributorpersonid[0])
            contributortypeid=session.query(ContributorType.field_lr_contributor_type_target_id).filter(ContributorType.entity_id==contributororgsval[0]).first()
            if contributortypeid is not None:
                contributortype=get_taxonomy_value(contributortypeid[0])
            contributororgs.append({'name':contributororg,'type':contributortype})
    j['contributor_orgs']=contributororgs


    jsondict['learning_resources'].append(j)

    

with open('IMLS.json', 'w') as outfile:
    json.dump(jsondict, outfile)
print("Done")