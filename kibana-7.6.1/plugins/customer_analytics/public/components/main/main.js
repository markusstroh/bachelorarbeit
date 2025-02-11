/**
 * IMPORTANT:
 * This file was generated by kibana like most of the part of the custom plugin. All functions
 * besides render() and componentDidMount() were added by the developer. Also, the HTML code
 * in the render() function was generated by kibana and modified by the developer.
 */

import React from 'react';
import {
  EuiPage,
  EuiPageHeader,
  EuiTitle,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentHeader,
  EuiPageContentBody,
  EuiText,
  EuiForm,
  EuiFormRow,
  EuiButton,
  EuiFlexGroup,
  EuiIconTip,
  EuiTable,
  EuiTableHeaderCell,
  EuiTableBody,
  EuiFieldNumber,
  EuiFlexItem
} from '@elastic/eui';

export class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      response : '',
      ruleArray: null,
      minSupport: 0,
      minConfidence: 0,
    };
  }

  /**
   * Send the request to the server in order to execute associationRuleMiner.py. Since values for minsupport and minconfidence <= 0 would result in infinite loops,
   * there is a check that the values are bigger than 0. The response of the server is a string containing the assiciation rules. This String needs to be processed
   * to print the rules with their values for support and confidence in a table.
   */
  async getRules(){
    if (this.state.minSupport > 0 && this.state.minConfidence > 0) {
      const {httpClient} = this.props
      await httpClient.get(`../api/customer_analytics/server/associationRuleMiner.py?minsupp=${this.state.minSupport}&minconf=${this.state.minConfidence}`).then((response) => {
        this.setState({time: response.data.time, response: response.data.data });
      });
    
      var splitRules = this.state.response.toString().split('\n');

      this.setState({ruleArray: splitRules});

      var htmlStr = '';

      for (var i = 0; i< splitRules.length-1; i++){
        var rule = splitRules[i].substring(0,splitRules[i].lastIndexOf("]")+1);

        var rest = splitRules[i].substring(splitRules[i].lastIndexOf("]")+3, splitRules[i].length);
        var metrics = rest.split(',');
      
        var support = metrics[0].trim().split(':')[1];
        var confidence = metrics[1].trim().split(':')[1];
      
        htmlStr += `<tr class="euiTableRow"><td class="euiTableRowCell"><div class=euiTableCellContent><span class="euiTableCellContent_text">${rule}</span></div></td>`;
        htmlStr += `<td class="euiTableRowCell"><div class=euiTableCellContent><span class="euiTableCellContent_text">${support}</span></div></td>`;
        htmlStr += `<td class="euiTableRowCell"><div class=euiTableCellContent><span class="euiTableCellContent_text">${confidence}</span></div></td></tr>`;
      }

      document.getElementById("tablebody").innerHTML = htmlStr;
    } else {
      window.alert("Minsupport and minconfidence must be greater than 0")
    }

  }


  setMinSupport(event){
    this.state.minSupport = event.target.value
  }


  setMinConfidence(event){
    this.state.minConfidence = event.target.value
  }

  /**
   * Sends the request to the server to execute transform.py. Prints result in window.alert.
   */
  transformData(){
    const { httpClient } = this.props;
    httpClient.get('../api/customer_analytics/server/transform.py').then((response) => {
      this.setState({ response: response.data.data });
      window.alert(this.state.response.output);
    });
  }

  componentDidMount() { 
    /*
       FOR EXAMPLE PURPOSES ONLY.  There are much better ways to
       manage state and update your UI than this.
    */
  }
  render() {
    const { title } = this.props;
    return (
      <EuiPage>
        <EuiPageBody>
          <EuiPageHeader>
            <EuiTitle size="l">
              <h1>Customer Analytics</h1>
            </EuiTitle>
          </EuiPageHeader>
          
          <EuiPageContent>
            <EuiPageContentHeader>
              <EuiTitle>
                <h1>Transforming Data</h1>
              </EuiTitle>
            </EuiPageContentHeader>
            <EuiPageContentBody>
              <EuiText>
                <p>In order to properly analyse the customer behavior the data needs to be trnasformed. To do so please press the Transform Data Button. You will recieve a message when the transformation is done.</p>
              </EuiText>
              <EuiForm >
                <EuiButton  fill onClick={() => this.transformData()}>
                  Transform Data
                </EuiButton>
              </EuiForm>
            </EuiPageContentBody>
          </EuiPageContent>
          
          <EuiPageContent>
            <EuiPageContentHeader>
              <EuiTitle>
                <h1>Association Rules</h1>
              </EuiTitle>
            </EuiPageContentHeader>
            <EuiPageContentBody>
              <EuiText>
                <p>This section can be used to mine association rules. To do so, please provide a minimum value for the support and confidence.</p>
              </EuiText>
              <EuiFlexGroup>
                <EuiFlexItem>
                  <EuiFormRow label="Minsupport" id="minSupportRow">
                    <EuiFieldNumber step={0.01} max={1} min={0.1} id="minSupportField" onChange={(event) => this.setMinSupport(event)}></EuiFieldNumber>
                  </EuiFormRow>
                </EuiFlexItem>
                <EuiFlexItem>
                  <EuiFormRow label="Minconfidence">
                    <EuiFieldNumber step={0.01} max={1} min={0.1} id="minConfidenceField" onChange={(event) => this.setMinConfidence(event)}></EuiFieldNumber>
                  </EuiFormRow>
                </EuiFlexItem>
                <EuiFlexItem>
                  <EuiFormRow hasEmptyLabelSpace>
                    <EuiButton fill onClick={() => this.getRules()} id="rulebutton">
                      Find rules
                    </EuiButton>
                  </EuiFormRow>
                </EuiFlexItem>
              </EuiFlexGroup>
              <EuiFlexGroup>
              <EuiTable>
                <EuiTableHeaderCell>Rule</EuiTableHeaderCell>
                <EuiTableHeaderCell>Support
                  <EuiIconTip content="The support describes how many times the itemset occured in all sessions" position="right"/>
                </EuiTableHeaderCell>
                <EuiTableHeaderCell>Confidence
                  <EuiIconTip content="The confidence of a rule A => B describes the probability that B appears in a Session if A appeared" position="right"/>
                </EuiTableHeaderCell>
                <EuiTableBody id="tablebody">
                </EuiTableBody>
              </EuiTable>
              </EuiFlexGroup>
            </EuiPageContentBody>
          </EuiPageContent>
        </EuiPageBody>

      </EuiPage>
    );
  }

}
