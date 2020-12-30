import React from 'react'
import PropTypes from 'prop-types';

class AvailableSeries extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            series_list: this.props.series_list
        }

     this.renderSeriesList = this.renderSeriesList.bind(this);
     this.playerInGame = this.playerInSeries.bind(this)
     this.renderPlayer = this.renderPlayer.bind(this)

    }

    componentWillReceiveProps(newProp) {
        this.setState({ series_list: newProp.series_list })
    }

    playerInSeries(series){
        var player = series.players.find(obj => {
            return obj.username === this.props.player.username
         })
        return player != null
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


    renderSeriesList() {
        // clear out series owned by this player
        let player_removed = this.props.series_list.filter(function(series) {
//             return series.creator.id !== this.props.player.id
            return ! this.playerInSeries(series)
        }, this);


        if (player_removed.length > 0) {
            return player_removed.map(function (series) {
                    return <li key={series.id} className="list-group-item">
                        <span className="badge pull-left">{series.id}</span>&nbsp; &nbsp;
                        (<span>{this.renderPlayer(series,1)}</span> and <span>{this.renderPlayer(series,3)}</span>)  &nbsp; &nbsp;  vs  &nbsp; &nbsp;  (<span>{this.renderPlayer(series,2)}</span> and <span>{this.renderPlayer(series,4)}</span>)
                        <a className="btn btn-sm btn-primary pull-right" href={"/series/"+series.id+"/"}>Join</a>
                    </li>
            }, this)

        } else {
            return ("No Available Series")
        }
    }

    render() {
        return (
            <div>
                <div className="panel panel-primary">
                    <div className="panel-heading">
                        <span>Available Series</span>
                    </div>
                    <div className="panel-body">
                        <div>
                            <ul className="list-group series-list">
                                {this.renderSeriesList() }
                            </ul>
                        </div>
                    </div>
                </div>

            </div>
        )
    }
}

AvailableSeries.defaultProps = {

};

AvailableSeries.propTypes = {
    series_list: PropTypes.array,
    player: PropTypes.object

};


export default AvailableSeries