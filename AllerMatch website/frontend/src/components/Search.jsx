/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/alt-text */
import React, { Component } from "react";
import M from "materialize-css";

export default class Search extends Component {
  componentDidMount() {
    M.AutoInit();
  }
  render() {
    return (
      <div className="container">
        <span>
          <h2>Allermatch allergen finder: Input Form</h2>
          This webpage features the following three ways of analysis to identify
          a relationship between your input sequence and an allergen from the
          database:
          <ul>
            <li>
              <b>80-amino-acid sliding window:</b> The input sequence is chopped
              up in 80-amino-acid windows. For each 80- amino acid window, the
              program counts which allergen it hits (with a specific identity).
            </li>
            <li>
              <b>Full Alignment:</b> Use FASTA to perform a full alignment.
            </li>
            <li>
              <b>Wordmatch:</b> Look for an exact hit of 6 or more contiguous
              amino acids in a sequence in the database.
            </li>
          </ul>
          As explained under{" "}
          <a class="modal-trigger" data-target="modal1">
            databases
          </a>
          , comparisons can be run against either of the following two
          databases:
          <ol>
            <li>
              The <b>AllergenDB_propeptides_removed</b> databases contains
              allergen sequences from which the signal- and propeptide sequences
              are removed when post-translational modifications (PTMs) were
              predicted by UniProtKB.
            </li>
            <li>
              The <b>AllergenDB_original_sequences</b> database contains the
              non-processed allergen sequences with PTMs.
            </li>
          </ol>
        </span>
        <br />
        <form
          name="allerform"
          enctype="application/x-www-form-urlencoded"
        >
          <input type="hidden" name="against" value="" />
          <table celspacing="0" cellpadding="5" width="100%">
            <tbody>
              <tr>
                <td colspan="2">
                  <b>Copy-paste your amino acid sequence here:</b>
                </td>{" "}
              </tr>
              <tr>
                <td colspan="2">
                  <textarea name="seq" rows="4" cols="80"></textarea>
                </td>{" "}
              </tr>
              <tr>
                <td colspan="2">
                  <b>Algorithm:</b>
                </td>
              </tr>
              <tr>
                <td colspan="1">
                  <input type="radio" name="method" value="window" checked="" />
                  Do an 80-amino-acid sliding window alignment
                </td>{" "}
                <td colspan="1">
                  <input
                    type="text"
                    name="cutOff"
                    size="10"
                    maxlength="8"
                    value="35"
                  />
                  Cut-off Percentage (only applicable to the 80-amino-acid
                  sliding window)
                </td>{" "}
              </tr>
              <tr>
                <td colspan="1">
                  <input type="radio" name="method" value="wordmatch" />
                  Look for a small exact wordmatch
                </td>{" "}
                <td colspan="1">
                  <input
                    type="text"
                    name="wordlength"
                    size="10"
                    maxlength="8"
                    value="6"
                  />
                  Wordlength (only applicable to the exact wordmatch search)
                </td>{" "}
              </tr>
              <tr>
                <td colspan="1">
                  <input type="radio" name="method" value="full" />
                  Do a full FASTA alignment
                </td>{" "}
              </tr>
              <tr>
                <td>
                  <b>Select a database:</b>
                </td>
                <td>
                  {" "}
                  <select name="database">
                    {" "}
                    <option value="AllergenDB_propeptides_removed" selected="">
                      AllergenDB_propeptides_removed
                    </option>
                    <option value="AllergenDB_original_sequences">
                      AllergenDB_original_sequences
                    </option>
                  </select>
                </td>
              </tr>
              <tr>
                <td colspan="2">
                  <input name=" Go " value="Go" type="submit" />
                </td>{" "}
              </tr>
            </tbody>
          </table>
        </form>
        {/* Modals used for displaying information about references are below. */}
        <div id="modal1" class="modal">
          <div class="modal-content">
            <h3>
              Allermatch<sup>tm</sup> database
            </h3>
            Allermatch<sup>tm</sup> contains the entries of three databases of
            known allergenic proteins that have been listed by:
            <ol>
              <li>
                {" "}
                The UniProt Protein Knowledgebase (
                <a href="http://www.uniprot.org/docs/allergen">UniProtKB</a>)
              </li>
              <li>
                {" "}
                The list of allergen nomenclature of the joint World Health
                Organization and International Union of Immunological Societies
                (<a href="http://www.allergen.org">WHO-IUIS</a>)
              </li>
              <li>
                {" "}
                The Comprehensive Protein Allergen Resource (
                <a href="http://comparedatabase.org">COMPARE</a>)
              </li>
            </ol>
            Signal- and pro-peptides are automatically removed from the allergen
            sequences based on the predictions of post-translational
            modifications (PTMs) provided by UniProtKB prior to the addition of
            sequences to the Allermatch<sup>tm</sup> database (
            <b>AllergenDB_propeptides_removed</b>). This processing of sequences
            is in compliance with the recommendations of the FAO/WHO Expert
            Consultation on the evaluation of potential allergenicity of
            genetically modified foods (2001;{" "}
            <a href="http://www.who.int/foodsafety/publications/biotech/en/ec_jan2001.pdf">
              link
            </a>
            ) in preparation of the Codex alimentarius' guidelines for the
            safety assessment of foods derived through biotechnology. This is an
            outstanding, characteristic feature of the Allermatch<sup>tm</sup>{" "}
            website as compared to other service providers. It helps users to
            ensure their compliance with the abovementioned recommentations and
            thereby avoid false positive outcomes that would otherwise be caused
            by alignments with pro- and signal-peptide segments. The{" "}
            <b>AllergenDB_original_sequences</b> database contains the
            non-processed allergen sequences with PTMs, and is provided as a
            separate database in Allermatch<sup>tm</sup>. Users can select the
            AllergenDB database with the non-processed sequences for comparisons
            with their query sequence, yet should be aware of the fact that this
            can yield additional alignments with pro- and signal-peptides still
            attached to the stored sequences.
            <br />
            <br />
            <h4>UniProt</h4>
            The UniProt list of allergens refers to accessions on the UniProt
            website, which contain well-annotated sequences.
            <br />
            <br />
            <h4>WHO-IUIS</h4>
            The WHO-IUIS list contains allergens, for example, maize allergen
            Zea m 14, each of which has been subdivided into one or more
            isoallergens. These isoallergens are allergenic proteins from the
            same source that show minor differences, such as single amino acid
            substitutions (for example, Zea m 14.0101 and Zea m 14.0102). This
            list contains allergenic proteins that have been registered
            following submission, for example by scientists who have discovered
            a new allergen. For registration, the allergenic protein should
            comply with certain requirements, such as a minimal number of
            patients that have shown reactivity towards this protein, as well as
            a minimal prevalence (5 percent) of reactivity among these patients.
            WHO-IUIS provides references to accessions in the UniProt and
            GenBank/GenPept sequence databases, which have consequently been
            used by Allermatch
            <sup>tm</sup>. The annotation of the sequences obtained from sources
            other than UniProt may not always provide details to the same level
            as in UniProt accessions.
            <br />
            <br />
            <h4>COMPARE</h4>
            The Comprehensive Protein Allergen Resource is a new comprehensive
            repository of protein sequences of known or putative allergens. It
            was created via the development of an automated rule-based sorting
            algorithm tool, combined with a review of the literature associated
            with the identified sequences. An independent peer-review panel of
            allergy experts exclusively from the public sector decides on the
            final content of the database. These three rigorous and well
            documented processes have been carefully designed to meet the needs
            for allergy safety assessment. The combination of these three
            processes has resulted in the new COMPARE database released on 03
            February 2017. The database includes a comprehensive repository of
            all known allergens, with the addition of newly identified
            allergens.
          </div>
          <div class="modal-footer">
            <a href="#!" class="modal-close waves-effect waves-green btn-flat">
              Close
            </a>
          </div>
        </div>
      </div>
    );
  }
}
