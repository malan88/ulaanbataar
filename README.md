Ulaanbataar
===========

I. Prospectus
=============
Ulaanbataar is a platform for finding financially actionable correlated
timeseries to seek alpha through exploitable random correlations.

The idea finds its genesis in two suppositions in Nassim Nicholas Taleb's book
Fooled by Randomness. They are:

1. Non-causal correlations exist. In an aside while ranting about the way
   traders get fooled by randomness in backtesting historical data for
   algotrading he suggests that he's convinced that there is a stock somewhere
   that perfectly correlates with temperature fluctuations of Ulaanbataar,
   Mongolia.
2. When you observe a thing (a time-dependent trend, that is, e.g. the staying
   power of a writer like Shakespeare's works) you are most likely to be
   observing it at the midpoint.

Given these two suppositions, we can infer the following:

If you observe an exploitable, random, non-causal correlation, it is most likely
to continue at least as far in the future as it has already lasted in the past.

So our goal is simple: to find actionable correlation, and to exploit it.

II. Possible Investigable Time Series
=====================================
This list is far from exhaustive. It is expected to expand and change.

1. Weather-related
    - Temperature
    - Precipitation
    - Pollution levels
    - Visiblity
    - Cloud cover
    - Pollen count
    - Global averages of the aforementioned
    - Regional averages of the aforementioned
2. Entertainment
    - Total box office sales
    - Streaming statistics
    - Box office/streaming performance of a given actor, director, or studio
    - Similar performance for a genre (science fiction, drama, etc.)
    - Similar statistics as the aforementioned for books, music, visual art,
      etc.
3. Sports
    - Performance of various teams, athletes, coaches
    - Points scored per day in a given sport.
4. Politics
    - Performance of particular political parties on election day
    - Performance of particular politicians on election day
    - Approval ratings of the aforementioned
    - Partisan lean of institutions
    - Partisan lean of legislation passed on a given day
5. Health
    - Prices for insurance premiums
    - Prices for CPT codes
    - Seasonal infection rates for the flu
    - Mortality/birth rates in various regions, states, countries, cities
6. Manufacturing
    - Item output (e.g., semiconductors)
    - Resource output (e.g., cobalt)
    - Production rates for a given company
    - Production rates for a given industry
7. Economics
    - Unemployment data
    - Any measure. Literally, any measure.
8. Markets
    - Stock price offsets (e.g. [StockA-1day] => [StockB])
    - Moving average offsets
    - Price/Earnings averages
    - Stocks whose earnings predictions most closely match actual earnings.

III. Architecture
=================
This is going to be a massive operation programmatically. We are essentially
performing one operation on infinite comparables: for any given two time series,
we want the offset covariance.

There are three main components to this software platform:

1. Data Gatherers & Data Harvesters
2. Data storage
3. Data analysis

Since the data being analyzed is so vastly heterogenous we will require
infrastructure in both code and hardware. The operations involved are not, in
fact, very complex, so most of it (if not all of it) can be automated.

For hardware, to begin with, I want something small and quiet so it can run 24/7
without disturbing me.  I have chosen to begin with a Raspberry Pi 4 with a 256
gigabyte microSD card running Arch Linux. In time this may (read:will
inevitably) become insufficient. We can expand this infrastructure model by
purchasing more Raspberry Pi's and converting to networked storage. Race
conditions may become a problem at that point. Eventually we may expand to cloud
servers.

For the software we are essentially writing our own libraries.

III.1 Data Gatherers & Data Harvesters
-----------------------------------

### 1. Gatherers

After writing my first threaded, source-heterogenous web scraper I believe this
will not be hard so much as tedious.

A central, inheritable, threaded class will serve as the basis for each unique
gatherer/harvester. It will provide a system for

1. Requesting the source.
2. Parsing the source, and
3. Storing the data.

This system will have to become progressively more complex and abstract. I would
like to be able to gather easily and extensibly from the following three types
of sources:

1. Simple scraping sources using `requests` and `BeautifulSoup4`. This will be
   fragile and therefore require some method for data validation and ensuring
   proper functioning.
2. JavaScript-execution-dependent web data, like Single Page Web Apps. We will
   use Selenium and headless Chromium. This is something I've never really done
   and will therefore require more investigation, but does not seem overly
   difficult. It will also require similar data validation and failure
   notifications.
3. JSON-based API data. This will actually be simplest. And most robust. Weather
   data and stock data seems easy by this route.

The gatherers will also require a system for exponential backoff and rate limit
maximization. I do not want to overload a source, but I also don't want to waste
access. Two algorithms for rate limits are comonly used:

1. Token-based systems: API calls are charged a predefined (and sometimes
   variable) token rate. The account generates a specified number of tokens per
   interval (usually a minute). There is usually an API route for the token
   status of the account that can be relied upon (for free) for the current
   token status of the account.
2. Hard rate limits: These typically specify a certain number of requests per
   time interval (5 per minute, 100,000 per month).

Most of these requirements (an exponential backoff system, a rate limit or token
limit system) can be defined as Mixins through multiple inheritance.

### 2. Harvesters

So far I have been desribing Gatherers: bots which gather predefined data
distributed from a given source. The other method of data collection is through
Harvesters: bots designed to generate data themselves over a period of time.

For instance, a bot might track volume and sentiment of tweets about a specific
ticker. This will take at least 100 days to become viable, but the time series
will be generated, or "harvested," not gathered.

Because this is more complex, and not easily specifiable ahead of time, this
section will remain brief, to serve mostly as a stub for future development.

III.2 Data Storage
==================
First, I will be using an ORM for convenience's sake, specifically SQLAlchemy
since it is widely adaptable and I am most familiar with it. If it becomes
unwieldy, I will abandon it and write my own ORM, which should not be difficult.

Second, I will use a full relational database system, most likely Postgresql.
Perhaps we would be better off with a NoSQL solution like Mongo or similar, but
given my unfamiliarity with such products, I will refrain for now. I plan to
design the system abstracted enough that I don't have to worry about switching
platforms easily.

Third, the simplest way to store any time series is as a JSON object in a TEXT
field. So the actual data generated will be stored as just a single field that
can be interpreted by `json.loads()`. It can thence be easily translated into a
pandas dataframe.

The object itself (table) should have numerous fields that can be extensible.

1. The source of the data (url? Harvesters would be more complex).
2. Type (Stock, temperature/city, etc. etc.)
3. Time frame: the interval of the actual data (DateTime to DateTime). This
   might be two fields Start and End, inclusive:exclusive for consistency's
   sake.
4. The actual data, stored as a JSON TEXT field.

The second object (table) is a comparison object that points the two objects it
compares. This will consist of the following fields:

1. Series1 points to the first object
2. Series2 points to the second object
3. A covariance field (or set of fields) which show the covariance of the two
   time series objects. This will perhaps be a JSON TEXT field itself, showing
   the expanding covariance window starting from the last date extending
   backwards.

III.3 Data Analysis
===================
This is the simplest process of the three, but will be far more computationally
expensive because of combinatorial explosion. We will have to write in ways of
tracking progress to find metrics to improve performance.

This idea will be to write a single class that can be multithreaded to compare
every stock time series to every other time series to find a covariance level
given a set of offsets.

The process will be, in its most simple form,

1. Normalize the time series
2. Starting with the shortest, most recent interval and expanding backward,
   create a covariance matrix.
3. Store the interval/covariance matrix series as a new object pointing to the
   two parent time series.
