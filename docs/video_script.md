# Capstone Video Script (Under 3 Minutes)

Hi, I’m Francisco Revelles, and this is my Capstone project for the Google AI Agents Intensive.

I built a multi-agent system that reads synthetic legal evidence, generates timelines, and answers questions about what happened in a case.

The goal is simple: legal analysis is hard because evidence is scattered across filings, emails, notes, and messages. Agents are great at reading text, but they need structure. So I created a pipeline that transforms raw files into a clean, chronological narrative.

Let me show you how it works.

First, there’s an MCP server called the Synthetic Evidence Server. It lists evidence files, returns the text of each file, and provides reproducible SHA-256 hashes so everything is deterministic.

Next, I have four agents: an Ingest Agent, an Analysis Agent, a Timeline Agent, and a Q&A Agent.

The Ingest Agent retrieves the evidence and normalizes it.  
The Analysis Agent extracts dates, actors, and key events.  
The Timeline Agent merges these fragments into an ordered sequence.  
And the Q&A Agent answers questions by looking at both the memory bank and the timeline.

To demonstrate all of this, I built a simple CLI interface.

You can list evidence, view the timeline, and ask questions like:  
“What happened after the February 4 email?”  
The system pulls from multiple agents to produce a clean answer.

The entire project uses only synthetic cases—no personal or real evidence.

Finally, everything is contained in a deterministic pipeline so results are reproducible. This is essential in legal and compliance workflows.

In the future, this foundation will be extended into the private LexFabric MDLS version, where it will connect with Alfresco, Notion, and multi-docket litigation workflows.

Thank you for watching, and I hope you enjoy the demo.
