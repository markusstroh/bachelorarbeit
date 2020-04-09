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
  EuiFieldText,
  EuiForm,
  EuiFormRow,
  EuiButton,
} from '@elastic/eui';

export class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchTerm :'',
      response : ''
    };
  }
  onSearchTextChange(event) {
    this.state.searchTerm = event.target.value;
  }

  searchData(){
    console.log("fick dich")

    /*const { httpClient } = this.props;
    httpClient.get('../api/test_plugin/search_test').then((response) => {
      this.setState({ response: response.data });
      window.alert(this.state.response);
    });*/
    window.alert(this.state.data.hits.hits[0]._source.userid)
  }
  componentDidMount() {
    /*
       FOR EXAMPLE PURPOSES ONLY.  There are much better ways to
       manage state and update your UI than this.
    */
    
    const { httpClient } = this.props;
    httpClient.get('../api/test_plugin/example').then(resp => {
      this.setState({ time: resp.data.time, data: resp.data.data });
      console.log("JAWOLL ALDER");
      console.log(this.state.data.hits.hits[0]._source.userid);
      console.log(this.state.data)
    });
  }
  render() {
    const { title } = this.props;
    return (
      <EuiPage>
        <EuiPageBody>
          <EuiPageHeader>
            <EuiTitle size="l">
              <h1>{title} Hello World!</h1>
            </EuiTitle>
          </EuiPageHeader>
          <EuiPageContent>
            <EuiPageContentHeader>
              <EuiTitle>
                <h2>Congratulations</h2>
              </EuiTitle>
            </EuiPageContentHeader>
            <EuiPageContentBody>
              <EuiText>
                <h3>You have successfully created your first Kibana Plugin!</h3>
                <p>The server time (via API call) is {this.state.time|| 'NO API CALL YET'}</p>
              </EuiText>
              <EuiForm >
                <EuiFormRow
                  label="Search Field"
                  helpText="Please enter search value"
                >
                  <EuiFieldText name="search_term" onChange={(event) => this.onSearchTextChange(event)}/>
                </EuiFormRow>

                <EuiButton  fill onClick={() => this.searchData()}>
                  Search
                </EuiButton>

              </EuiForm>
            </EuiPageContentBody>
          </EuiPageContent>
        </EuiPageBody>
        <EuiPageBody>
          <EuiPageContent>
            <EuiPageContentHeader>
              <EuiTitle>
                <h2>neue box</h2>
              </EuiTitle>
            </EuiPageContentHeader>
            <EuiPageContentBody>
              <EuiText>
                <h3>Yfsdfsad</h3>
                <p>Tfgsdfdsafasd</p>
              </EuiText>
              <form>
               <label for="fname">First Name</label><br></br>
                <input type="text" id="fname" name="fname"></input>
              </form>
            </EuiPageContentBody>
          </EuiPageContent>
        </EuiPageBody>
      </EuiPage>
    );
  }

}
