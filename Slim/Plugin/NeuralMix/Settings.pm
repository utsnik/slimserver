package Slim::Plugin::NeuralMix::Settings;

use strict;
use base qw(Slim::Settings::Base);

use Slim::Utils::Prefs;

my $prefs = preferences('plugin.neuralmix');

sub name { 'PLUGIN_NEURALMIX' }

sub page { 'plugins/NeuralMix/settings.html' }

sub prefs {
	return ($prefs, qw(brain_url auto_vectorize));
}

sub handler {
	my ($class, $client, $params, $callback, @args) = @_;
	return $class->SUPER::handler($client, $params, $callback, @args);
}

1;
