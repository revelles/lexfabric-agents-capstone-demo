Hi, I’m Francisco Revelles, and this is my Capstone project for the Google AI Agents Intensive.

I built a multi-agent system that reads synthetic legal evidence, generates timelines, and answers grounded questions about what happened in a case.

The core problem is that evidence is fragmented across filings, emails, notes, and incident logs. Reconstructing a sequence of events is slow and error-prone. Agents are good at interpreting text, but they need structure—so I built a pipeline that transforms raw files into a chronological narrative.

Here’s how it works.

The system starts with the Synthetic Evidence Server.
It lists synthetic evidence files, returns their text, and provides SHA-256 hashes for reproducible, deterministic runs.

On top of that, the system uses several narrowly scoped agents:

The Evidence Agent loads evidence records and raw text from the synthetic evidence server.

The Timeline Agent extracts event fragments, identifies dates, and builds an ordered timeline.

The Memory Bank stores normalized entities, summaries, and events so agents can retrieve consistent information during reasoning.

The Q&A Agent answers natural-language questions by combining memory lookups with timeline traversal—grounded strictly in the loaded evidence.

And the Router orchestrates which agent runs based on the CLI mode, whether you’re listing evidence, building the timeline, or asking a question.

To demonstrate all of this, I built a small CLI interface.

You can load a synthetic case, view all evidence, generate the timeline, and ask questions like:
“What happened first?”
or
“What event occurred after the initial note?”

The system walks the timeline and the memory bank to produce an answer tied directly to evidence—never hallucinated.

The entire dataset is 100% synthetic for the Capstone and safe for public demonstration.

Everything runs offline, using a deterministic pipeline with SHA-256 hashing. This is essential for legal, compliance, and investigative workflows where reproducibility and provenance matter.

In the future, this foundation will expand into the private LexFabric MDLS, where it will support multi-docket reasoning, Alfresco integration, and more sophisticated evidence workflows.

Thanks for watching, and I hope you enjoy the demo.