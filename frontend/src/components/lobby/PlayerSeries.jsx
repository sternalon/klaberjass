import React from 'react'
import PropTypes from 'prop-types';

class PlayerSeries extends React.Component{
  constructor(props) {
      super(props)
      this.state = {
        series_list: this.props.series_list
      }

      // bind button click
     this.onCreateSeriesClick = this.onCreateSeriesClick.bind(this);
     this.renderButton = this.renderButton.bind(this);
     this.renderPlayer = this.renderPlayer.bind(this)
     this.playerInSeries = this.playerInSeries.bind(this)
    }

    onCreateSeriesClick(event) {
        this.props.sendSocketMessage({action: "create_series"})
    }


    componentWillReceiveProps(newProp){
        this.setState({series_list: newProp.series_list})
    }

    playerInSeries(series){
        var player = series.players.find(obj => {
            return obj.username === this.props.player.username
         })
        return player != null
        }

    renderButton(series){
         if (series.completed){
            return "View"
// TODO: I think that these lines and playerInSeries can be removed.
//         } else if (series.opponent == null && series.creator.id == this.props.player.id){
//         } else if (series.players.length < 4 && this.playerInSeries(series)){
//             return "Waiting..."
         } else{
             return "Play"
         }

    }

    renderPlayer(series, position){
         var player = series.players.find(obj => {
            return obj.position === position
         })

        if (player != null){
            return player.username
        } else {
            return "Player ".concat(position.toString())
        }
    }


    renderSeriesList(){
        if (this.props.series_list.length > 0){
            return this.props.series_list.map(function(series){
                    return <li key={series.id} className="list-group-item">
                                <span className="badge pull-left">{series.id}</span>&nbsp;&nbsp;
                                (<span>{this.renderPlayer(series,1)}</span> and <span>{this.renderPlayer(series,3)}</span>)  &nbsp; &nbsp;  vs  &nbsp; &nbsp;  (<span>{this.renderPlayer(series,2)}</span> and <span>{this.renderPlayer(series,4)}</span>)

                                <a className="btn btn-sm btn-primary pull-right" href={"/series/"+series.id+"/"}>{this.renderButton(series)}</a>
                            </li>
                    }, this)

        }else{
            return ("No Series")
        }
    }

    render() {
      return (
        <div>
          <div className="panel panel-primary">
                <div className="panel-heading">
                    <span>Your Series</span>
                    <a href="#" className="pull-right badge" onClick={this.onCreateSeriesClick} id="create_series">Start New Series</a>
                </div>
                <div className="panel-body">
                    <div>
                        <ul className="list-group series-list">
                            {this.renderSeriesList()}
                        </ul>
                    </div>
                </div>
            </div>

        </div>
      )
    }
}

PlayerSeries.defaultProps = {

};

PlayerSeries.propTypes = {
    series_list: PropTypes.array,
    player: PropTypes.object
};


export default PlayerSeries