package Slim::Control::Provider;

use strict;
use warnings;

use Slim::Utils::Log;

my $log = logger('control.command');

sub init {
	my $class = shift;

	my @providers = qw(
		Alarms
	);

	for my $p (@providers) {
		my $module = "Slim::Control::Provider::$p";
		
		main::INFOLOG && $log->info("Loading provider: $module");

		eval "require $module";
		if ($@) {
			$log->error("Failed to load provider $module: $@");
			next;
		}

		if ($module->can('register')) {
			$module->register();
		}
	}
}

1;
