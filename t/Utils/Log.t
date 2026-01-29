#!/usr/bin/perl

use strict;
use warnings;
use FindBin qw($Bin);
use lib "$Bin/../..";      # Root directory for Slim::*

use Test::More;
use lib "$Bin/../../CPAN"; # Bundled dependencies

# Mock Log4perl to avoid dependency issues with binary components
BEGIN {
    $INC{'Log/Log4perl.pm'} = 1;
    $INC{'Log/Log4perl/Logger.pm'} = 1;
    $INC{'Log/Log4perl/Appender/Screen.pm'} = 1;
    $INC{'Log/Log4perl/Appender/File.pm'} = 1;
    
    {
        package Log::Log4perl::Logger;
        sub new { return bless {}, shift }
        sub get_logger { return Log::Log4perl::Logger->new() }
        sub error { }
        sub warn { }
        sub info { }
        sub debug { }
        sub is_debug { return 0 }
        sub is_info { return 0 }
    }

    {
        no strict 'refs';
        *Log::Log4perl::init = sub {};
        *Log::Log4perl::get_logger = sub {
            return Log::Log4perl::Logger->new();
        };
        *Log::Log4perl::initialized = sub { return 1 };
    }

    # Mock other requirements
    $INC{'Slim/Utils/OSDetect.pm'} = 1;
    {
        no strict 'refs';
        *Slim::Utils::OSDetect::getOS = sub {
            return bless {}, 'MockOS';
        };
        *MockOS::logRotate = sub {};
        *Slim::Utils::OSDetect::dirsFor = sub { return "." };
    }

    # Define constants in main
    {
        no strict 'refs';
        *main::ISWINDOWS = sub { 0 };
        *main::DEBUGLOG  = sub { 0 };
        *main::INFOLOG   = sub { 0 };
        *main::SCANNER   = sub { 0 };
        *main::RESIZER   = sub { 0 };
        *main::TRANSCODING = sub { 0 };
        *main::STATISTICS = sub { 0 };
        *main::SB1SLIMP3SYNC = sub { 0 };
        *main::WEBUI = sub { 0 };
        *main::ISMAC = sub { 0 };
        *main::NOMYSB = sub { 1 };
        *main::PERFMON = sub { 0 };
        *main::ISUNIX = sub { 1 };
    }
}

use Slim::Utils::Log qw(logger logWarning logError);

subtest 'logger' => sub {
    my $log = logger('test_category');
    ok(defined($log), 'logger returns defined object');
    isa_ok($log, 'Log::Log4perl::Logger');
};

subtest 'logWarning' => sub {
    # Initialize the class to set $rootLogger
    Slim::Utils::Log->init({});
    
    eval { logWarning('test warning') };
    ok(!$@, 'logWarning did not die');
};

done_testing();
