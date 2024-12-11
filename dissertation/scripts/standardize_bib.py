import re
import sys

# Define the journal mapping: full names to abbreviations
JOURNAL_MAPPING = {
    "American Journal of Epidemiology": "Am. J. Epidemiol.",
    "Anaesthesia, Critical Care & Pain Medicine": "Anaesth. Crit. Care Pain Med.",
    "BMC Biology": "BMC Biol",
    "Bayesian Analysis": "Bayes. Anal.",
    "Bioinformatics": "Bioinformatics",
    "Cell Host & Microbe": "Cell Host Microbe",
    "Cell Reports Medicine": "Cell Rep. Med.",
    "China CDC Weekly": "China CDC Wkly.",
    "Distill": "Distill",
    "Emerging Infectious Diseases": "Emerg. Infect. Dis.",
    "Eurosurveillance": "Eurosurveillance",
    "Evolution": "Evolution",
    "Expert Review of Anti-Infective Therapy": "Expert Rev. Anti Infect. Ther.",
    "Infectious Diseases of Poverty": "Infect. Dis. Poverty",
    "Journal of Open Source Software": "J. Open Source Softw.",
    "Journal of Machine Learning Research": "J. Mach. Learn. Res.",
    "Journal of Statistical Software": "J. Stat. Softw.",
    "Lancet Public Health": "Lancet Public Health",
    "Nature": "Nature",
    "Nature Genetics": "Nat. Genet.",
    "Nature Microbiology": "Nat. Microbiol.",
    "Nature Reviews Genetics": "Nat. Rev. Genet.",
    "Nature Reviews Microbiology": "Nat. Rev. Microbiol.",
    "Nature Communications": "Nat. Commun.",
    "New England Journal of Medicine": "N. Engl. J. Med.",
    "PLOS Computational Biology": "PLoS Comput. Biol.",
    "PLOS ONE": "PLoS ONE",
    "PLOS Pathogens": "PLoS Pathog.",
    "PeerJ Computer Science": "PeerJ Comput. Sci.",
    "Proceedings of the National Academy of Sciences": "Proc. Natl. Acad. Sci. USA",
    "Proceedings of the Royal Society A": "Proc. R. Soc. A",
    "Proceedings of the Royal Society B": "Proc. R. Soc. B",
    "SIAM Review": "SIAM Rev.",
    "SIAM Journal on Applied Mathematics": "SIAM J. Appl. Math.",
    "Science": "Science",
    "Science Translational Medicine": "Sci. Transl. Med.",
    "Scientific Data": "Sci. Data",
    "Statistics and Computing": "Stat. Comput.",
    "The American Naturalist": "Am. Nat.",
    "The Lancet Infectious Diseases": "Lancet Infect. Dis.",
    "Theoretical Population Biology": "Theor. Popul. Biol.",
    "Trends in Microbiology": "Trends Microbiol.",
    "Virus Evolution": "Virus Evol.",
    "Wellcome Open Research": "Wellcome Open Res.",
    "arXiv": "arXiv",
    "bioRxiv": "bioRxiv",
    "eLife": "eLife",
    "medRxiv": "medRxiv",
}


def extract_braced_content(field_line, field_name):
    """Extracts the content of a BibTeX field, handling nested braces."""
    # Match the field and extract its content, accounting for nested braces
    match = re.search(rf"{field_name}\s*=\s*({{.*}}|\".*\")", field_line, re.DOTALL)
    if match:
        content = match.group(1)
        # Strip the outer braces or quotes
        if content.startswith("{") and content.endswith("}"):
            content = content[1:-1]
        elif content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        return content
    return None


def normalize_journal_name(journal_name):
    """Normalize journal names for consistent comparison."""
    # Remove LaTeX escape characters, trim whitespace, and lowercase
    journal_name = re.sub(r"\\&", "&", journal_name)
    return journal_name.strip().lower()


def standardize_journal_name(journal_name):
    """Standardizes journal names based on the mapping."""
    normalized_name = normalize_journal_name(journal_name)
    for full_name, abbreviation in JOURNAL_MAPPING.items():
        if normalized_name in (
            normalize_journal_name(full_name),
            normalize_journal_name(abbreviation),
        ):
            return abbreviation
    return None  # Indicates an unknown journal


def extract_title_content(line):
    """Extracts the full title content, preserving nested braces."""
    match = re.search(r"title\s*=\s*({.*}|\".*\")", line, re.DOTALL)
    if match:
        content = match.group(1)
        if content.startswith("{") and content.endswith("}"):
            return content[1:-1]  # Strip outermost braces
        elif content.startswith('"') and content.endswith('"'):
            return content[1:-1]  # Strip outermost quotes
    return None


def capitalize_proper_nouns(title):
    """Capitalizes specific proper nouns in a title, leaving bracketed words untouched."""
    proper_nouns = [
        "New York",
        "Markov",
        "Gaussian",
        "March",
        "Erlang",
        "June",
        "SARS-CoV-2",
        "Omicron",
        "Beta",
        "Delta",
        "COVID",
        "IgG",
        "Netherlands",
        "Europe",
        "South Korea",
    ]  # Extend as needed

    for noun in proper_nouns:
        # Add brackets and capitalize if not already bracketed
        title = re.sub(
            rf"(?<!{{)(?<![\w{{])({re.escape(noun)})(?![\w}}])(?!}})",
            r"{\1}",  # Wrap the match in braces
            title,
            flags=re.IGNORECASE,
        )
    return title


def process_entry(entry_lines, citation_key, author_cutoff=6):
    """Processes a single BibTeX entry, handling authors and preserving LaTeX formatting."""
    fields = "".join(entry_lines)
    updated_lines = []
    missing_fields = []
    primary_fields = {
        "author",
        "title",
        "journal",
        "year",
        "volume",
        "pages",
        "publisher",
    }

    # Check for missing fields once
    if "year =" not in fields:
        missing_fields.append("year")
    if "volume =" not in fields:
        missing_fields.append("volume")

    # Log missing fields
    if missing_fields:
        print(f"Missing {', '.join(missing_fields)} in entry '{citation_key}'")

    for line in entry_lines:
        # Extract field name
        field_match = re.match(r"\s*(\w+)\s*=", line)
        if field_match:
            field_name = field_match.group(1).lower()

            # Skip non-primary fields
            if field_name not in primary_fields:
                continue

        # Standardize journal names
        if line.strip().startswith("journal ="):
            match = re.search(
                r'journal\s*=\s*[{"\'](.+?)[}"\']', line.strip(), re.IGNORECASE
            )
            if match:
                journal_name = match.group(1).strip()
                standardized_name = standardize_journal_name(journal_name)
                if standardized_name:
                    line = re.sub(re.escape(journal_name), standardized_name, line)
                else:
                    print(
                        f"Warning: Unknown journal '{journal_name}' in entry '{citation_key}'"
                    )

        # Capitalize proper nouns in titles
        if line.strip().startswith("title ="):
            title_content = extract_title_content(line)
            if title_content:
                modified_title = capitalize_proper_nouns(title_content)
                line = re.sub(
                    r"title\s*=\s*({.*}|\".*\")",
                    f"title = {{{modified_title}}}",
                    line,
                    flags=re.DOTALL,
                )

        # Trim the number of authors
        if line.strip().startswith("author ="):
            match = re.search(
                r'author\s*=\s*[{"\'](.+?)[}"\']', line.strip(), re.IGNORECASE
            )
            if match:
                authors = match.group(1).strip()
                # Respect LaTeX commands and braces
                authors_list = re.split(r"\s+and\s+", authors)
                if len(authors_list) > author_cutoff:
                    # Trim authors and add et al.
                    trimmed_authors = (
                        " and ".join(authors_list[:author_cutoff]) + " and others"
                    )
                    # Rebuild the author field
                    line = re.sub(
                        r'author\s*=\s*[{"\'].*?[}"\']',
                        f"author = {{{trimmed_authors}}}",
                        line,
                        flags=re.IGNORECASE,
                    )

        # Remove month and issue
        line = re.sub(
            r",\s*month\s*=\s*[{\"'].*?[}\"']\s*", "", line, flags=re.IGNORECASE
        )
        line = re.sub(
            r",\s*number\s*=\s*[{\"'].*?[}\"']\s*", "", line, flags=re.IGNORECASE
        )

        updated_lines.append(line)

    return updated_lines


def clean_bibtex(input_file, output_file):
    """Processes a BibTeX file to clean and standardize entries."""
    with open(input_file, "r") as file:
        bib_content = file.readlines()

    output_content = []
    entry_lines = []
    citation_key = None

    for line in bib_content:
        if line.strip().startswith("@"):
            # Process the previous entry
            if entry_lines:
                output_content.extend(process_entry(entry_lines, citation_key))
                entry_lines = []
            # Start a new entry
            citation_key = re.search(r"@\w+\{(.+?),", line)
            citation_key = citation_key.group(1) if citation_key else "Unknown"
            output_content.append(line)
        elif citation_key:
            # Accumulate lines for the current entry
            entry_lines.append(line)
        else:
            output_content.append(line)

    # Process the last entry
    if entry_lines:
        output_content.extend(process_entry(entry_lines, citation_key))

    # Save the updated BibTeX file
    with open(output_file, "w") as file:
        file.writelines(output_content)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_bibtex.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        clean_bibtex(input_file, output_file)
