# Generic IEEE submission layer

Source of truth remains the bilingual Markdown under paper/modules and paper/modules_parts, with paper/references/library.bib and the manifest-registered CSV and figure assets. Files under paper/builds/ieee_generic are generated and must not be edited by hand.

Generate the English IEEE candidate:

    python paper/submission/ieee_generic/build_submission.py --lang en --compile

Generate the bilingual paragraph-paired review build:

    python paper/submission/ieee_generic/build_submission.py --lang bilingual --compile

The same SourceReader and Markdown AST renderer serve both variants. English uses pdflatex when available. Bilingual uses xelatex plus xeCJK and an automatic generic CJK font fallback. No font path or font file is committed.

Each generated directory contains `main.tex`, section files, editable generated tables, the two registered figures, a generated copy of `library.bib`, `IEEEtran.cls`, and `build_manifest.json`. The manifest records source hashes, stable IDs, validation results, and the build-specific compile status. On the audited MiKTeX environment, both builds compile through the explicit engine/BibTeX fallback: English is 14 pages and bilingual is 22 pages. Both static validations pass.

The default author mode is anonymous_placeholder. Camera-ready mode is available through --mode camera_ready, but generation is rejected until structured author entries are supplied in submission_config.yaml. USER_DECISION_REQUIRED: keywords.

The English build is intended for future venue adaptation. The bilingual build is BILINGUAL_REVIEW_BUILD for internal review and EN/ZH consistency checking; it is not claimed to satisfy an IEEE submission-language policy.

Venue, track, anonymous policy, reference page accounting, appendix policy, supplement policy, and abstract limit remain UNKNOWN. IEEEtran.bst is not bundled; it must resolve from the TeX runtime and did resolve in the audited MiKTeX environment. The script probes `latexmk` before use, falls back to explicit engine/BibTeX runs when needed, and does not install missing components.

When a concrete venue is selected, adapt the config and main template to its official package and rules, then regenerate. Do not edit files under `paper/builds/ieee_generic` directly.
