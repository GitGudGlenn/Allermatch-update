/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/alt-text */
import React from "react";

export default function Howto(props) {
  return (
    <div>
      <span>
        <h1>
          Behind Allermatch<sup>tm</sup>
        </h1>
        This webtool has been constructed through a joint effort of{" "}
        <a href="https://www.wur.nl/nl/Onderzoek-Resultaten/Onderzoeksinstituten/food-safety-research.htm">
          WFSR - Wageningen University and Research
        </a>{" "}
        and{" "}
        <a href="http://www.wur.nl/en/Expertise-Services/Research-Institutes/plant-research/Bioscience.htm">
          Bioscience - Wageningen University and Research
        </a>
        .
        <p>
          WFSR is specialised in food safety research, including the safety of
          genetically engineered foods and animal feed. For example, WFSR
          develops advanced methods for detection- and safety testing- of
          genetically engineered foods. In addition, WFSR advises national and
          international authorities on the safety of genetically engineered
          foods and feed.
        </p>
        <p>Participants for WFSR in this project are</p>
        <ul>
          <li>
            {" "}
            Dr. ir. Gijs A. Kleter (
            <a href="mailto:gijs.kleter@wur.nl">gijs.kleter@wur.nl</a>)
          </li>
          <li>
            {" "}
            Dr. A.A.C.M. Peijnenburg (
            <a href="mailto:ad.peijnenburg@wur.nl">ad.peijnenburg@wur.nl</a>).
          </li>
          <li>
            {" "}
            Dr. ir. Martijn Staats (
            <a href="mailto:martijn.staats@wur.nl.nl">martijn.staats@wur.nl</a>)
          </li>
        </ul>
        The web server software is written in
        <a href="http://www.python.org"> Python&nbsp;</a> and is hosted by an
        <a href="http://httpd.apache.org"> apache webserver</a> using
        <a href="http://www.modpython.org/"> mod_python</a>.
      </span>
    </div>
  );
}
