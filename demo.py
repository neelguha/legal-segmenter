from legal_segmenter.segmenter import Segmenter


# Load input data
text = """   Rule 23 does not set forth a mere pleading standard. A party seeking class certification must affirmatively demonstrate his compliance with the Rule—that is, he must be prepared to prove that there are in fact sufficiently numerous parties, common questions of law or fact, etc. We recognized in Falcon that “sometimes it may be necessary for the court to probe behind the pleadings before coming to rest on the certification question,” 457 U. S., at 160, and that certification is proper only if “the trial court is satisfied, after a rigorous analysis, that the prerequisites of Rule 23(a) have been satisfied,” id., at 161; see id., at 160 (“[A]ctual, not presumed, conformance with Rule 23(a) remains … indispensable”). Frequently that “rigorous analysis” will entail some overlap with the merits of the plaintiff ’s underlying claim. That cannot be helped. “ ‘[T]he class determination generally involves considerations that are enmeshed in the factual and legal issues comprising the plaintiff ’s cause of action.’ ” Falcon, supra, at 160 (quoting Coopers & Lybrand v. Livesay, 437 U. S. 463, 469 (1978); some internal quotation marks omitted). Nor is there anything unusual about that consequence: The necessity of touching aspects of the merits in order to resolve preliminary matters, e.g., jurisdiction and venue, is a familiar feature of litigation. See Szabo v. Bridgeport Machines, Inc., 249 F. 3d 672, 676–677 (CA7 2001) (Easterbrook, J.)."""

# Print out each sentence extracted
seg = Segmenter()
paragraphs = seg.segment(text)
for paragraph in paragraphs:
    for sentence in paragraph:
        print(sentence.strip())
