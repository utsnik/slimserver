package Slim::Control::Provider::Alarms;

use strict;
use warnings;

use Slim::Control::Request;
use Slim::Control::Commands;
use Slim::Control::Queries;

sub register {
	# alarm <cmd>
	Slim::Control::Request::addDispatch(['alarm', '_cmd'], [1, 0, 1, \&Slim::Control::Commands::alarmCommand]);

	# alarm playlists <index> <quantity>
	Slim::Control::Request::addDispatch(['alarm', 'playlists', '_index', '_quantity'], [0, 1, 1, \&Slim::Control::Queries::alarmPlaylistsQuery]);

	# alarms <index> <quantity>
	Slim::Control::Request::addDispatch(['alarms', '_index', '_quantity'], [1, 1, 1, \&Slim::Control::Queries::alarmsQuery]);
}

1;
