/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/alt-text */
import React from "react";
import "../CSS/App.css";

export default function Howto(props) {
  return (
    <div>
      <span>
        <h1>
          How to use Allermatch<sup>tm</sup>
        </h1>
        <h4>Input sequence</h4>
        <p>
          The following sequence is that of the mature protein of the allergen
          Zea m 14.0101 from maize pollen. As may be noticed, this sequence
          contains a one-letter code for each amino acid, while the complete
          sequence is made up of 93 letters or amino acids:
        </p>
        <p>
          <mark>
            aiscgqvasaiapcisyargqgsgpsagccsgvrslnnaarttadrraacnclknaaagvsglnagnaasipskcgvsipytiststdcsrvn
          </mark>
        </p>
        <p>
          While the original protein sequence in the UniProt database entry
          P19656 consisted of 120 amino acids, removal of the signal peptide
          comprising the first 27 amino acids has yielded this mature protein
          sequence containing 93 amino acids.
        </p>
        <p>
          If users enter their own input sequences, numbers in this sequence
          should be removed, whereas spaces, paragraph- or line- returns, need
          not be removed. In addition, three-letter codes for amino acids, such
          as IleSerCys... (first 3 residues of Zea m 14) should be changed into
          one-letter codes, for example by using web-based conversion tools (for
          example,
          <a href="http://bioinformatics.org/sms2/three_to_one.html">
            "Three-to-One"
          </a>
          ).
        </p>
        <h4>
          Entering an input sequence and selecting the alignment of interest
        </h4>
        <p>
          Enter the input sequence, by typing or copy-pasting it, in the
          searchbox (below "Copy Paste your amino acid sequence here") of the
          Allermatch<sup>tm</sup> search page. With the cursor, select one of
          the following options:
        </p>
        <ul class="browser-default">
          <li>"Do an 80-amino-acid sliding window alignment"</li>
          <li>"Look for a small exact wordmatch"</li>
          <li>"Do a full fasta alignment"</li>
        </ul>
        <p>
          In case the 80-amino-acid sliding windows has been chosen, the default
          threshold value of 35% identity may be modified by the user in the box
          next to "Cut-off Percentage (only applicable to the 80-amino-acid
          sliding window)". The threshold is the lower limit for alignments that
          will be displayed in the following steps (alignments scoring below the
          threshold will therefore not be displayed).{" "}
        </p>
        <p>
          If the option for a small exact wordmatch has been chosen, the default
          value 6 for the wordlength can be modified by the user in the box next
          to " Wordlength (only applicable to the exact wordmatch search)". The
          wordlength is the minimal number of amino acids in an exact match.
        </p>
        <p>
          After having selected the options and thresholds (if applicable) of
          interest, click then the "Go" button. The results will appear in the
          new page that is created in the same window on the user's screen. The
          various outcomes are discussed below for each of the specific options.
        </p>
        <ul class="collapsible">
          <li>
            <div class="collapsible-header">
              <i class="material-icons">arrow_forward</i>80-amino-acid sliding
              window
            </div>
            <div class="collapsible-body">
              <span>
                <h4>Summary table</h4>
                The new page that appears after starting the 80-amino-acid
                sliding window alignment on the input sequence provides a table
                with a summary of the "hits", which are alignments scoring above
                the cutoff value. Each specific allergenic protein whose
                database sequence scored hits is presented in a new line, while
                data on this allergenic protein and the alignment are presented
                under the following column headings:
                <ul class="browser-default">
                  <dl>
                    <dt>"Hit No"</dt>
                    <dd>
                      The rank of the best hit (see third column) of the
                      allergenic protein, such as 1, 2, or 3, while the rank for
                      the highest best hit is 1.
                    </dd>
                    <dt>"Db"</dt>
                    <dd>
                      Database from which the allergen sequence has been
                      retrieved.
                    </dd>
                    <dt>"Description"</dt>
                    <dd>
                      The description for the allergenic protein as provided by
                      UniProt/GenBank in the protein database accession.
                    </dd>
                    <dt>"Best hit (identity)"</dt>
                    <dd>
                      Highest number of identical amino acids in the hits,
                      expressed as percentage of 80- or more- amino acids, for
                      example 30% for 24 identical amino acids.
                    </dd>
                    <dt>"No of windows ident &gt;x"</dt>
                    <dd>
                      The number of amino-acid subsequences (windows) of the
                      input sequence that showed hits above the cut-off value
                      with the database sequence of the allergenic protein.
                    </dd>
                    <dt>"% of windows ident &gt;x "</dt>
                    <dd>
                      The fraction (percentage, %) of the total number of
                      analysed subsequences (windows) of the input sequence that
                      showed hits above the cutoff value with the allergenic
                      protein.
                    </dd>
                    <dt>"Full identity"</dt>
                    <dd>
                      Identical amino acids in the FASTA alignment of the
                      complete input sequence against the database sequence of
                      the allergenic protein. The first number is the percentage
                      of identical amino acids as part of the total length of
                      the alignment, while the second number is the total length
                      of this alignment expressed as number of amino acids
                      (including non-identical amino acids).
                    </dd>
                    <dt>"External link"</dt>
                    <dd>
                      The external accession id, which is clickable and provides
                      a link to the original accession for the database sequence
                      on the source database's website.
                    </dd>
                    <dt>"Scientific name"</dt>
                    <dd>
                      Latin name of the organism from which the allergenic
                      protein is derived.
                    </dd>
                    <dt>"Detailed information"</dt>
                    <dd>
                      The clickable "Go" button links to a page with specific
                      details on the database sequence of the allergenic
                      protein, as well as the complete FASTA alignment and the
                      subsequences (windows) of the input sequence aligning to
                      the database sequence. After having clicked on the "Go"
                      button, a new page will appear in the same window on the
                      user's screen.
                    </dd>
                  </dl>
                </ul>
                <h4>Detailed information</h4>
                This page provides the following information:
                <ul class="browser-default">
                  <li>The input sequence (amino acid sequence).</li>
                  <li>
                    Details on the database sequence of the allergenic protein,
                    including allergen name, species name, external accession
                    id, remarks (for example, signal-, pro-, or transit-
                    peptides that have been removed from the sequence) and amino
                    acid sequence.
                  </li>
                  <li>
                    The complete amino acid sequences of the input- and
                    database- sequences are shown in this page. Below each
                    one-letter code for amino acid residues in both of these
                    sequences, a "#"-marking may be displayed. The residues
                    marked with "#" were aligned with residues in the other
                    sequence (database or input, respectively) in the
                    80-amino-acid window alignments that had 35% or more
                    identical amino acids in the window. Please note that these
                    "#" markings also include nonidentical residues in both the
                    input- and database- sequences that were aligned to each
                    other. The 35% cut-off value is fixed for these "#" markings
                    and cannot be changed by the user.
                  </li>
                  <li>
                    Details of the full alignment between the complete input
                    sequence (no 80-amino-acid windows) and the allergenic
                    protein.
                  </li>
                </ul>
                By clicking the "Show all alignments" button all the separate
                hits, i.e. alignments of those 80-amino-acid subsequences
                (windows) of the input sequence that scored equal to- or above-
                the cut-off value of 35% (fixed value, cannot be changed by the
                user), can be viewed. The new page that appears in the same
                window on the user's screen contains the same information as the
                previous page, in addition to the separate hits. After clicking
                "Hide all alignments", the previous page re-appears.
                <h4>Example</h4>
                For the input sequence Zea m 14 screened against the Allermatch
                <sup>tm</sup> database, for example, the summary table lists
                various database sequences of allergenic proteins that score
                hits if the cut-off value equals 35%. Since the Zea m 14
                sequence contains 93 amino acids, 14 subsequences (windows) of
                80 amino acids have been generated (1-80, 2-81, ...., 13-92,
                14-93). The highest ranking database sequence in the table is
                Zea m 14 itself, because the same sequence has also been stored
                in the Allermatch<sup>tm</sup> database, which shows a best hit
                of 100%, while all of the 14 windows of the input sequence
                scored hits, as expected. One of the lower ranking sequences in
                the table is the allergenic protein Par j 2 derived from weed
                pollen from <i>Parietaria judaica</i>. The best hit for this
                sequence is 36.59% identity, while 4 of the 14 windows scored
                hits. The detailed information on the alignments with Par j 2
                show that a large part of both the input and database sequence
                are part of the 80-amino-acid sliding window- and full-
                alignments. Interestingly, many of the sequences listed in the
                table are lipid transfer proteins, as mentioned in the original
                external accession to which the table provides links.
              </span>
            </div>
          </li>
          <li>
            <div class="collapsible-header">
              <i class="material-icons">arrow_forward</i>Exact hits of small
              stretches of identical amino acids
            </div>
            <div class="collapsible-body">
              <span>
                <h4>Summary table</h4>
                The new page that appears after starting the alignment of small
                identical stretches using WordMatch provides a table summarising
                the "hits", which are the alignments equal to- or above- the
                wordlength, i.e. the minimal number of identical contiguous
                amino acids. Each of the database sequences of allergenic
                proteins that showed a hit with the input sequence is shown in a
                separate line of the table, while the data on the allergenic
                protein are shown under the following column headings:
                <ul class="browser-default">
                  <dl>
                    <dt>"No"</dt>
                    <dd>
                      Rank of the database sequence of the allergenic protein,
                      while the sequence that scores the highest number of
                      wordmatches ranks number 1.
                    </dd>
                    <dt>"Db"</dt>
                    <dd>
                      Database from which the allergen sequence has been
                      retrieved.
                    </dd>
                    <dt>"Description"</dt>
                    <dd>
                      The description of the allergenic protein as provided by
                      UniProt/GenBank in the protein database accession.
                    </dd>
                    <dt>"Number of exact wordmatches"</dt>
                    <dd>
                      The number of identical stretches of a given wordlength
                      shared by the input- and database- sequences.
                    </dd>
                    <dt>"% of exact wordmatches"</dt>
                    <dd>
                      The identical stretches of a given wordlength shared by
                      the input- and database- sequences, expressed as
                      percentage of the maximum number of stretches
                      (nonidentical and identical) of the same wordlength that
                      can be made from the input sequence.
                    </dd>
                    <dt>"External db"</dt>
                    <dd>
                      The external accession number, which is clickable and
                      provides a link to the original accession for the database
                      sequence on the source database website.
                    </dd>
                    <dt>"Scientific name"</dt>
                    <dd>
                      Latin name of the organism from which the allergenic
                      protein is derived.
                    </dd>
                    <dt>"Detailed information"</dt>
                    <dd>
                      After the "Go" button has been clicked on, a new page is
                      created in the same window on the user's screen that
                      contains information on the allergenic protein, and the
                      hits of short identical stretches.
                    </dd>
                  </dl>
                </ul>
                <h4>Detailed information</h4>
                This page provides the following information on the hits of the
                selected wordlength with a specific allergenic protein:
                <ul class="browser-default">
                  <li>The input sequence (amino acid sequence)</li>
                  <li>
                    Details on the database sequence of the allergenic protein,
                    including allergen name, scientific name, external accession
                    id and amino acid sequence.
                  </li>
                  <li>
                    The complete amino acid sequences of the input- and
                    database- sequences, while the "#"-symbols mark the residues
                    within these sequences that are part of the exact hits with
                    the wordlength of 6 amino acids (fixed wordlength, which
                    does not change to the wordlength entered by the user).
                  </li>
                  <li>
                    Matches that are shorter than 6 amino acids may be found in
                    the output of the full alignment (see below).
                  </li>
                </ul>
                <h4>Example</h4>
                For the Zea m 14 test sequence, tested against the Allermatch
                <sup>tm</sup>
                database, the summary table mentions various database sequences
                of allergenic proteins, including Zea m 14 itself, if a
                wordlength of 6 is selected. Besides Zea m 14, the other
                database sequences include, among others, allergenic proteins
                that are classified as lipid transfer proteins. Among the low
                ranking database sequences are Pru av 3 and Pru ar 3 from cherry
                and apricot, respectively, each of which scored one hit. As can
                be inferred from the detailed information, the single identical
                stretch of 6 amino acids (acnclk) in Pru av 3 and Pru ar 3 is
                also present in some of the other listed database sequences.
              </span>
            </div>
          </li>
          <li>
            <div class="collapsible-header">
              <i class="material-icons">arrow_forward</i>Full alignment
            </div>
            <div class="collapsible-body">
              <span>
                The new page that appears after starting the full alignment
                contains the following information:
                <ul class="browser-default">
                  <li>
                    Bar diagram showing the number of hits for certain
                    statistical scores (E, opt) of the FASTA alignments of the
                    input sequence with the database sequences of allergenic
                    proteins.
                  </li>
                  <li>
                    List of database sequences of allergenic proteins, ranked in
                    descending order of best statistical scores for the
                    alignment of these sequences with the input sequence.
                  </li>
                  <li>
                    Details of each specific alignment from the previous list,
                    in the same order.
                  </li>
                </ul>
                <h4>Example</h4>
                If Zea m 14 has been entered as input sequence, the highest
                scoring database sequences are the same as for the 80-amino
                acids sliding window alignment, i.e. lipid transfer proteins.
              </span>
            </div>
          </li>
        </ul>
      </span>
    </div>
  );
}
