# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): ...
- `size` (str): ...
- `max_price` (float): ...

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): ...
- `wardrobe` (dict): ...

**What it returns:**
<!-- Describe the return value -->

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->

---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (...): ...

**What it returns:**
<!-- Describe the return value -->

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->

---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | |
| suggest_outfit | Wardrobe is empty | |
| create_fit_card | Outfit input is missing or incomplete | |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     ASCII art, a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html), or an embedded
     sketch are all fine. You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

---


## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**

**Milestone 4 — Planning loop and state management:**

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

 FitFindr helps users discover secondhand clothing items, style them with pieces from their existing wardrobe, and generate shareable outfit content. The agent first searches available listings, then suggests an outfit using the selected item and the user's wardrobe, and finally creates a fit card suitable for social media. If no matching listing is found, the workflow stops and the user receives guidance on how to modify their search instead of proceeding with invalid data.

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->
-- > The agent first calls search_listings() to find clothing items that match the user's request.
     tool called : search_listings()
     input : description="vintage graphic tee",
               size="M",
               max_price=30.0

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->
-->
     The planning loop stores this item in session state as:

          state["selected_item"]

     output of step 1:
          {
               "id": 102,
               "title": "Faded Band Tee",
               "description": "Vintage-inspired oversized band graphic tee",
               "size": "M",
               "price": 22.00,
               "condition": "Good",
               "platform": "Depop",
               "style_tags": ["grunge", "vintage", "streetwear"]
          }

     The agent now calls tool suggest_outfit().
     The selected listing from Step 1 is passed along with the user's wardrobe.
     The wardrobe is loaded using:
          get_example_wardrobe()

     The tool analyzes colors, style tags, and clothing categories already present in the wardrobe.
     
     Output ex. : Pair the vintage band tee with your wide-leg jeans and platform Doc Martens for a classic 90s grunge look. Roll the sleeves once and loosely front-tuck the shirt for extra shape.

     The outfit suggestion is stored in:
          state["outfit"]

**Step 3:**
<!-- Continue until the full interaction is complete -->

--> The agent now generates social-media-ready styling text by calling create_fit_card().

     Tool Call:
     create_fit_card(
     outfit=outfit_suggestion
     )

     output : thrifted this faded band tee off depop for $22 and honestly it was made for my wide-legs 🖤full look in my stories

     stores res in state["fit_card"]


**Final output to user:**
<!-- What does the user actually see at the end? -->

-->     
     Best Match:
     Faded Band Tee — $22 (Depop)

     Suggested Outfit:
     Pair the vintage band tee with your wide-leg jeans and platform Doc Martens for a classic 90s grunge look. Roll the sleeves once and loosely front-tuck the shirt for extra shape.

     Fit Card:
     "thrifted this faded band tee off depop for $22 and honestly it was made for my wide-legs 🖤 full look in my stories"

     Source:
     Depop listing #102