# Insurance API

This is a sample Flask project composed of a few APIs, that demonstrate the use of Flask. 

## Provided APIs:

The provided APIs are the following:
* POST /register
* POST /login
* POST /insurances
* POST /recommendation

Below they are explained in more detail.

### Register

The register API receives an `email` and a `password` in its body and register a new user if the email is not already registered.

### Login

The login API also receives an `email` and a `password` and tries to log user in.

If the user is registered then it returns an `access_token, that is required by the recommendation API.

### Insurances

This API was written to allow easy inclusion of some `insurances`, only for the recommendation to work properly. 

It receives a list of insurances, with the fields `name` and `monthly_price`.

### Recommendation

This API requires and authenticated user to work, with the Authorization header filled with the user access token.
The body of the request is composed of the fields of a questionnaire:
* `first_name`
* `address`
* `children`
* `occupation`
* `email`

If the email passed is the same as the email which is logged in, then the user data is updated with the passed information, before requesting the insurance recommendation.

Otherwise it just returns the recommendation.

## Testing

The project provides a Postman environment and collection with samples for calling all the APIs.

### How to test

The insurance API must be called once with the new insurances, so they can be registered and later recommended.

If the insurances already exist, they will not be saved again.

Calling the recommendation API without saving the insurances will work, however it will return a list of empty results, since the recommendation is based on searching specific insurances for each variation of inputs.

## Trying it live

The project is deploy as a Docker container in an instance on Google Cloud Provider.

So it can be run directly from Postman by running the collection under the gcp folder.
