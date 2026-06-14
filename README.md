# FitFindr 

FitFindr is an AI-powered thrift fashion assistant that helps users discover clothing items, receive outfit recommendations, and generate social-media-style outfit captions. The system searches a mock clothing marketplace, selects the best matching item, suggests outfits based on the user's wardrobe, and creates a shareable "fit card" caption.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

```bash
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```


**Tool Inventory**

# Tool 1: search_listings
Purpose
  Searches the listings dataset and returns matching thrifted clothing items based on the user's description, size, and budget.

Function Signature
  search_listings( description: str, size: str | None = None, max_price: float | None = None ) -> list[dict]

Inputs
  Parameter	        Type	  Description
  description	      str	    User's clothing search query
  size	        str | None	Desired clothing size
  max_price	  float | None	Maximum acceptable price

Output
  list[dict]

  A list of matching listing dictionaries containing:
  id
  title
  description
  category
  style_tags
  size
  condition
  price
  colors
  brand
  platform
  
  Results are sorted by relevance score.

# Tool 2: suggest_outfit

Purpose
  Generates outfit recommendations using the selected thrifted item and the user's wardrobe.

Function Signature
  suggest_outfit( new_item: dict, wardrobe: dict ) -> str
  
Inputs
    Parameter	Type	Description
    new_item	dict	Selected clothing item from search results
    wardrobe	dict	User wardrobe containing an items list

Output
  str
  
  A natural-language outfit recommendation.
  If the wardrobe is empty, the tool provides general styling advice.


# Tool 3: create_fit_card

Purpose
  Creates a short social-media-style caption based on the outfit recommendation.

Function Signature
  create_fit_card( outfit: str, new_item: dict ) -> str
  
Inputs
    Parameter	Type	Description
    outfit	str	Outfit recommendation from suggest_outfit
    new_item	dict	Selected clothing item

Output
  str
  
  A 2–4 sentence caption suitable for Instagram or TikTok.


**Planning Loop**

The planning loop follows a conditional workflow:

Step 1: Create a new session dictionary.

Step 2: Parse the user query and extract:
            description
            size
            max_price
        Store these values in: session["parsed"]
            
Step 3: Call:
            search_listings()
        Store results in: session["search_results"]
            
Step 4: Check whether results were returned.
        If:
          len(results) == 0
        then:
          session["error"] = ..
          
        and return immediately.

        The agent does not continue to outfit generation.

Step 5: Select the top-ranked result.
        Store: session["selected_item"]
                
Step 6: Call:
            suggest_outfit(selected_item, wardrobe)
        Store: session["outfit_suggestion"]
              
Step 7: Call:
            create_fit_card(outfit_suggestion, selected_item)
        Store: session["fit_card"]
        
Step 8: Return the completed session.


**State Management**

The application uses a single session dictionary as the source of truth throughout the interaction.

  Stored values include:
    {
        "query": ...,
        "parsed": ...,
        "search_results": ...,
        "selected_item": ...,
        "wardrobe": ...,
        "outfit_suggestion": ...,
        "fit_card": ...,
        "error": ...
    }

# Data flows through the tools as follows:

search_listings
      ↓
selected_item
      ↓
suggest_outfit
      ↓
outfit_suggestion
      ↓
create_fit_card
      ↓
fit_card

The same selected item returned from search_listings is passed directly into suggest_outfit and create_fit_card.


**Error Handling Strategy**

# search_listings

Failure Mode
    No listings match the user's search criteria.

* Example Tested
  search_listings(
      "designer ballgown",
      size="XXS",
      max_price=5
  )
  
  Result
  []
  
  Agent Response
    No listings matched your search.
    Try a broader description,
    different size, or a higher budget.
    
    The planning loop stops immediately.

*suggest_outfit

Failure Mode
    Wardrobe is empty.

  * Example Tested
    suggest_outfit(
        results[0],
        get_empty_wardrobe()
    )
    
    Result
    Returns general styling advice instead of crashing.

    Example:
    Pair this vintage tee with relaxed jeans and chunky sneakers...

    The interaction continues successfully.


# create_fit_card

Failure Mode
    Outfit string is empty.

* Example Tested
  create_fit_card(
      "",
      results[0]
  )
  
  Result
  Returns a descriptive error message.

  Example:
  Error: Outfit suggestion is empty.
  Unable to generate fit card.
  
  No exception is raised.

**Spec Reflection** 

# How the Spec Helped
  The planning.md document forced me to define tool inputs, outputs, state transitions, and failure handling before implementation. This made it easier to implement the planning loop and test tools independently.


# How Implementation Diverged
  Originally I planned to use only exact keyword matching for search relevance. During implementation I expanded matching across title, description, category, style tags, and brand fields to improve search quality and return more useful results.


**AI Usage**

# Example 1 — Tool Implementation

Input Given to AI

I provided:
    Tool 1 specification from planning.md
    Function signature
    Required failure behavior
    Data loader requirements

Specifically:
    What search_listings should do
    Inputs and return values
    Requirement to use load_listings()
    
Output Produced
    The AI generated a keyword-scoring search function that:
      Loads listings
      Filters by size
      Filters by price
      Scores keyword overlap
      Sorts by relevance
    
    What I Changed
    I corrected field references and adjusted scoring logic after testing against the dataset.

# Example 2 — Planning Loop Implementation

Input Given to AI

I provided: 
    Planning Loop section
    State Management section
    Architecture diagram

Output Produced
    The AI generated a draft run_agent() implementation that:
        Created a session
        Called tools sequentially
        Stored state
        
    What I Changed
    I modified the code to:
        Stop execution when search_listings returned no results
        Store additional session values
        Improve error messages
        Verify state was correctly passed between tools

Testing confirmed that the no-results path exited early and did not call suggest_outfit or create_fit_card.

**Testing Summary**

Completed tests: 
      search_listings returns matching results
      search_listings returns empty list on impossible query
      search_listings respects price filtering
      suggest_outfit works with example wardrobe
      suggest_outfit works with empty wardrobe
      create_fit_card generates captions
      create_fit_card handles empty outfit input

Result:

7 passed in 2.12s

All required tool functionality and failure modes were verified before integrating the planning loop.

<img width="1198" height="793" alt="Screenshot 2026-06-14 at 00 26 12" src="https://github.com/user-attachments/assets/5ed28cfc-5255-4871-a17f-c1cfb9261f2a" />
