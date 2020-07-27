**Updates**:

- July 26, 2020: we'll just use a Python helper function that deletes all records of a content type before replacing them with fresh data. The function will wait for the scrapers to finish before executing.

# Summary

I think we should have custom controllers that handle everything related to writing data to Strapi. This will help contributors have an easier time developing for this project. Contributors would only need to focus on creating scrapers rather than focusing on resolving data differences between the Strapi instance and the college website. It'll look like this:

```
                      ┌── backend ──────────────────────────────────┐
                      │  ┌──────────┐     ┌──────────────────────┐  │
┌───────────────┐     │  │          │     │                      │  │
│  scraper_1    +-------->          +----->  custom controllers  │  │
└───────────────┘     │  │          │     │                      │  │
                      │  │          │     └──────────+───────────┘  │
┌───────────────┐     │  │          │                │              │
│  scraper_2    +-------->   auth   │                │              │
└───────────────┘     │  │          │     ┌──────────V───────────┐  │
                      │  │          │     │                      │  │
┌───────────────┐     │  │          │     │      strapi cms      +--------> internet
│  scraper_3    +-------->          │     │                      │  │
└───────────────┘     │  │          │     └──────────────────────┘  │
                      │  └──────────┘                               │
                      └─────────────────────────────────────────────┘
```

## Use Cases

We should make this because it will ensure that data that goes in Strapi follows the same mechanism. Contributors need not worry about implementing their own algorithms to check for differences between data in Strapi and the data they scraped.

## Risks

All authenticated scrapers will have the complete control over the data in Strapi. This means that anybody with a key can potentially overwrite data that they do not have responsibility for. Imagine a Python script that writes data to Clubs suddenly writing data to Courses. Apart from creating hyperspecific roles and permissions, the only thing we can do is trust that the scraper will not compromise the data. All scrapers will be reviewed before placing them in production to mitigate the risk.

The scrapers can either be hosted within the same machine as Strapi, or they can be deployed as discrete serverless services. I would rather have them run outside the same machine as Strapi, but it would be easier to execute them with a CRON script in the same machine.

## Implementation details

The only thing we need to develop are the custom controllers. Here's pseudocode:

```
if user sent malformed data or is missing an authentication key:
    return http error 400 (bad request response)

dataArray = the array of data entries the scraper sent to Strapi via a a POST request
recordsInStrapiArray = an array of records of a specific content type in Strapi

for each entry in dataArray:
    if entry from dataArray found in recordsInStrapiArray:
        if entry is the same:
            return
        if entry is different:
            overwriteRecord(entry, recordsInStrapiArray)

    if entry from dataArray not found in recordsInStrapiArray:
        createRecord(entry, recordsInStrapiArray)

for each record in recordsInStrapiArray:
    if record from recordsInStrapiArray was not matched with any entry from dataArray:
        deleteRecord(record, recordsInStrapiArray)
```

The idea here is that we only have to choose one of these operations for any given data entry: create record, update record, or delete record. We create a record for some entry not yet found in Strapi, update a record if the entry is found but is different, and delete records that did not get compared against any entry.

All of the customized controllers will be placed in `/backend/api/\*\*/controllers`. The data sent in via a POST request has to be an array of JSON, otherwise we return an HTTP 400 (bad request) error.
