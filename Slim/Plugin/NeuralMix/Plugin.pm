package Plugins::NeuralMix::Plugin;

use strict;
use base qw(Slim::Plugin::Base);

sub initPlugin {
	my $class = shift;
    warn "\n\nDEBUG: Plugins::NeuralMix Initialized!\n\n";
	return 1;
}

sub getDisplayName { 'NeuralMix (Plugins)' }

1;
