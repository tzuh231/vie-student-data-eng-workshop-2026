# Massar Capital Management: Data Engineering Student Analyst Workshop

## Workshop At A Glance

| | |
|---|---|
| Date and time | Thursday, November 19, 2026, 16:00-20:00 |
| Location | Massar Capital Vienna Office, Karntner Ring 4, 1010 Vienna, 1st Floor |
| Prerequisites | Python knowledge and a personal laptop |

The workshop evaluates how participants structure ambiguous problems, adapt as requirements evolve, reason about engineering trade-offs and assumptions, write and explain code, use AI appropriately, and communicate and collaborate.

## Agenda

| Time | Session | Purpose |
|---|---|---|
| 16:00-16:30 | Welcome and introduction | Introduce Massar, the team, data engineering in a hedge fund, and the workshop context; form teams. |
| 16:30-17:00 | Individual Assignment | Coding exercises in preparation of Group Assignment |
| 17:00-17:45 | Group Assignment Part 1: Data pipeline | Build the intraday data-processing pipeline. AI assistants are not permitted. |
| 17:45-18:30 | Group Assignment Part 2: Research dashboard | Build an interactive Streamlit dashboard. AI assistants are permitted. |
| 18:30-19:30 | Group presentations | Each team presents its solution, followed by questions. |
| 19:30-20:00 | Wrap-up | Sample solution and demonstration |

## Case Study

### Context

You have joined the Data Engineering team at Massar Capital.
Researchers rely on historical intraday equity prices to analyze market behavior and develop trading strategies. Currently, they export raw market data to Excel and manually produce summaries at different time intervals.
This process has become increasingly difficult to maintain. Data can arrive out of order, contain duplicates, have missing observations, or be corrected after publication.
Your team has been asked to develop a reliable Python-based system that processes raw 1-minute records into reliable 5-minute bars, dependable market data for research.
- Part 1 (45 minutes; no AI): Build the intraday data-processing pipeline.
- Part 2 (45 minutes; AI permitted): Build an interactive Streamlit research dashboard.

We are interested in your ability to design a sensible solution, implement it correctly, and explain your decisions. A focused, working implementation is preferable to a large unfinished system.

### Market Data
Each source observation describes the price and trading activity for one stock over a one-minute interval.


| Term | Meaning |
|---|---|
| Ticker | Identifier for the security, such as AAPL or MSFT |
| Timestamp | Start of the observation interval |
| Open | First traded price during the interval |
| High | Highest traded price during the interval |
| Low | Lowest traded price during the interval |
| Close | Last traded price during the interval |
| Volume | Number of shares traded during the interval |
| OHLCV | Shorthand for Open, High, Low, Close, and Volume |
| Candle / bar | A summary of observations over a defined interval |

The fields Open, High, Low, Close, Volume are commonly abbreviated as OHLCV.
A five-minute candle summarizes five consecutive one-minute intervals. A candle labeled 09:30 covers the one-minute observations beginning at 09:30, 09:31, 09:32, 09:33, and 09:34.

## Prompt 1: Data Pipeline

**45 minutes | AI assistants are not permitted**

**Context:** The research team needs a repeatable way to transform external market observations into a consistent dataset. They have given you access to some real data they are using in `data/raw`

**Task:** Develop a pipeline that converts the supplied 1-minute market observations into trustworthy stored 1-minute and 5-minute OHLCV datasets.

**Discussion Only:** Suppose the pipeline must eventually run every trading day and expand from a couple of instruments to over a thousand. How would you scale your implementation?


## Prompt 2: Research Dashboard

**45 minutes | AI assistants are permitted**

**Context:** The research team has started using the historical datasets produced by your pipeline. Until now, researchers had primarily worked with five-minute market data via dashboards. Different analyses, however, require examining price movements at different time horizons. The team now wants to explore the same market data at 1-minute, 5-minute, 15-minute, 30-minute, and 1-hour frequencies through a single internal application in Streamlit.

In addition, researchers would like to measure the **Rolling Realized Volatility** of each equity, using a window of 30 consecutive 1-minute returns.

The logarithmic return at minute $i$ is:

$$
r_i = \ln\left(\frac{C_i}{C_{i-1}}\right)
$$

The Rolling Realized Volatility is calculated as:

$$
RV_t = 100 \times \sqrt{\sum_{i=t-29}^{t} r_i^2}
$$

Where:

- $RV_t$: Rolling Realized Volatility at time $t$, expressed as a percentage (not annualized).
- $r_i$: Logarithmic return at minute $i$, calculated as $\ln(C_i/C_{i-1})$.
- $i$: Index running over the 30 most recent 1-minute returns.
- $t$: Index of the latest observation.

**Task:** Develop a snappy and fast Streamlit candle chart dashboard that allows researchers to:
-	Select a ticker and trading date
-	Switch among 1m, 5m, 15m, 30m, and 1h bars frequencies seamlessly.
- Display Rolling Realized Volatility as a line chart below the candlestick chart, aligned by timestamp.

**Discussion Only:** Imagine the dashboard now covers the 1,000 tickers and all their history from Part 1 and is used by multiple researchers throughout the trading day. How would you scale the implementation and its infrastructure?

## Group Presentations

**10–15 MINUTES TOTAL (INCLUDING Q&A)**

Each group will present its solution to the research team, covering:

- **System Design:** Walk through your implementation with a diagram or flowchart, highlighting your key design decisions.
- **Live Demonstration:** Show your Streamlit dashboard, including switching between tickers, dates, and frequencies, and displaying the realized volatility indicator.

### Q&A

- **Infrastructure:** Your pipeline currently runs locally. How would you deploy it so that it runs automatically every trading day? What services or infrastructure would you need?
- **Scaling:** What would you change if you needed to process data for 1,000 tickers and their history?
- **Storage:** Would you continue storing the data as local files, or would you move to a database or object storage? Why?
- **Dashboard performance:** Suppose 20 researchers are using your Streamlit dashboard simultaneously. What are the likely bottlenecks, and how would you address them?
- **Data freshness:** If an upstream provider corrects a historical observation, how would you ensure the pipeline, stored datasets, caches, dashboard, and realized volatility values all reflect the correction?
- **Reliability:** What happens if the daily ingestion job fails halfway through? How would you recover without introducing duplicates or inconsistent data?
## Deliverables

Each team should submit:

- A pull request or merge request containing its work.
- Presentation support material, such as a PDF, PowerPoint, or system diagram.
