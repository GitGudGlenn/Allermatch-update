/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/alt-text */
import "../CSS/image.css";
import React from "react";
import allermatchLogo from "../img/allermatch_logo.png";

export default function Application() {
  return (
    <div>
      <span>
        <h1>
          Welcome to Allermatch<sup>tm</sup>
        </h1>
        <img className="logo" ALIGN="Right" src={allermatchLogo} />

        <p>
          Allermatch<sup>tm</sup> is a unique webtool which compares the amino
          acid sequence of a protein of interest against a database filled with
          sequences of know allegenic proteins. This webcool carries out the
          procedure of predicting the potential allergenicity of your provided
          proteins by following bioinformatics approaches as recommended by the
          Codex alimentarius and the FAO/WHO Expert consultation on
          allergenicity of foods derived through modern biotechnology [
          <a class="modal-trigger" data-target="modal1">
            1
          </a>
          ,
          <a class="modal-trigger" data-target="modal2">
            2
          </a>
          ]. The unique features of the Allermatchtm webtool allows the users to
          enter their input sequences in a time saving and user friendly way.
          After selecting your required options and hitting the search button.
          The webtool will provide an easy to read PDF file containing the
          results, written in an accurate, concise and comprehensible format.
        </p>

        <li>
          Allermatch<sup>tm</sup> contains 2277 polypeptide sequences (2070
          UniProt ids, 26 UniProt ids with multiple polypeptide chains, and 207
          GenBank RefSeqProtein ids).
        </li>
        <li>
          The Allermatch<sup>tm</sup> database (AllergenDB) was constructed
          using the combined and unique UniProt and GenBank NCBI protein
          accessions from COMPARE (Comprehensive Protein Allergen Resource),
          UniProt and the WHO/IUIS Allergen database.
        </li>
        <li>The COMPARE database was last accessed on 31 March 2021</li>
        <li>
          The UniProt allergen database was last accessed on 31 March 2021
        </li>
        <li>
          The WHO/IUIS Allergen database was last accessed on 31 March 2021
        </li>

        <p>
          We have had this website made to share our knowlegde and our developed
          program with others within this field of research. By continuing to
          update the databases behind this website and upgrade this tool with
          new features we hope to help others with their work, as it helped us
          with our work. Since maintaning this website and the tool and server
          behind it does cost us money. The website itself is not free to use.
          You can apply for an account and wait for our approval by signing up
          and sending us an e-mail. We're always willing to work something out
          so it will be beneficial for the both of us.
        </p>
      </span>

      {/* Modals used for displaying information about references are below. */}
      <div id="modal1" class="modal">
        <div class="modal-content">
          <h4>Codex Alimentarius Commission</h4>
          <p>
            Codex Alimentarius Commission (2003) Guideline for the Conduct of
            Food Safety Assessment of Foods derived from Recombinant-DNA Plants
            (CAC/GL 45-2003). Rome: Codex Alimentarius, Joint FAO/WHO Food
            Standards Program. Available at:{" "}
            <a href="http://www.fao.org/fileadmin/user_upload/gmfp/docs/CAC.GL_45_2003.pdf">
              http://www.fao.org/fileadmin/user_upload/gmfp/docs/CAC.GL_45_2003.pdf
            </a>
          </p>
          <p>
            This document recommends the following sequence comparisons between
            transgenic and allergenic proteins:
            <br />
            <cite>
              8. The purpose of a sequence homology comparison is to assess the
              extent to which a newly expressed protein is similar in structure
              to a known allergen. This information may suggest whether that
              protein has an allergenic potential. Sequence homology searches
              comparing the structure of all newly expressed proteins with all
              known allergens should be done. Searches should be conducted using
              various algorithms such as FASTA or BLASTP to predict overall
              structural similarities. Strategies such as stepwise contiguous
              identical amino acid segment searches may also be performed for
              identifying sequences that may represent linear epitopes. The size
              of the contiguous amino acid search should be based on a
              scientifically justified rationale in order to minimize the
              potential for false negative or false positive results*. Validated
              search and evaluation procedures should be used in order to
              produce biologically meaningful results.
              <br />
              9. IgE cross-reactivity between the newly expressed protein and a
              known allergen should be considered a possibility when there is
              more than 35% identity in a segment of 80 or more amino acids
              (FAO/WHO 2001) or other scientifically justified criteria. All the
              information resulting from the sequence homology comparison
              between the newly expressed protein and known allergens should be
              reported to allow a case-by-case scientifically based evaluation.
              <br />* It is recognized that the 2001 FAO/WHO consultation
              suggested moving from 8 to 6 identical amino acid segments in
              searches. The smaller the peptide sequence used in the stepwise
              comparison, the greater the likelihood of identifying false
              positives, inversely, the larger the peptide sequence used, the
              greater the likelihood of false negatives, thereby reducing the
              utility of the comparison.
            </cite>
          </p>
        </div>
        <div class="modal-footer">
          <a href="#!" class="modal-close waves-effect waves-green btn-flat">
            Close
          </a>
        </div>
      </div>

      <div id="modal2" class="modal">
        <div class="modal-content">
          <h4>FAO/WHO</h4>
          <p>
            FAO/WHO (2001) Joint FAO/WHO Expert Consultation on Foods Derived
            from Biotechnology - Allergenicity of Genetically Modified Foods -
            Rome, 22 - 25 January 2001. Rome: Food and Agriculture Organisation
            of the United Nations. <br />
            <a href="http://www.who.int/foodsafety/publications/biotech/en/ec_jan2001.pdf">
              http://www.who.int/foodsafety/publications/biotech/en/ec_jan2001.pdf
            </a>
          </p>
        </div>
        <div class="modal-footer">
          <a href="#!" class="modal-close waves-effect waves-green btn-flat">
            Close
          </a>
        </div>
      </div>
      {/* End of the Modals */}
    </div>
  );
}
