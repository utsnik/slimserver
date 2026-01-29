#!/usr/bin/perl

use strict;
use warnings;
use FindBin qw($Bin);
use lib "$Bin/../..";      # Root directory for Slim::*

use Test::More;
use lib "$Bin/../../CPAN"; # Bundled dependencies (added after Test::More)

# Mock dependencies to allow loading in an environment without LMS binaries
BEGIN {
    # Mock Logic for Log and Prefs across namespaces
    $INC{'Slim/Utils/Log.pm'} = 1;
    $INC{'Slim/Utils/Prefs.pm'} = 1;
    {
        no strict 'refs';
        my $mock_logger = sub { 
            return bless {}, 'MockLogger';
        };
        *Slim::Utils::Log::logger = $mock_logger;
        *Slim::Utils::Misc::logger = $mock_logger; # LMS uses it like a local sub often
        
        my $mock_prefs = sub {
            return bless {}, 'MockPrefs';
        };
        *Slim::Utils::Misc::preferences = $mock_prefs;
        *Slim::Utils::Prefs::preferences = $mock_prefs;

        *MockLogger::error = sub {};
        *MockLogger::warn  = sub {};
        *MockLogger::info  = sub {};
        *MockLogger::debug = sub {};
        *MockLogger::is_debug = sub { 0 };
        *MockLogger::is_info  = sub { 0 };
        
        *MockPrefs::get = sub { return "" };
        *MockPrefs::set = sub {};
        *MockPrefs::setChange = sub {};
    }

    # Mock Digest::SHA1
    $INC{'Digest/SHA1.pm'} = 1;
    {
        no strict 'refs';
        *Digest::SHA1::sha1_hex = sub { return "mock_sha1" };
    }

    # Mock other requirements that might fail
    $INC{'Slim/Music/Info.pm'} = 1;
    $INC{'Slim/Player/ProtocolHandlers.pm'} = 1;
    $INC{'Slim/Utils/DateTime.pm'} = 1;
    $INC{'Slim/Utils/Strings.pm'} = 1;
    $INC{'Slim/Utils/Unicode.pm'} = 1;

    # Mock OSDetect
    $INC{'Slim/Utils/OSDetect.pm'} = 1;
    {
        no strict 'refs';
        *Slim::Utils::OSDetect::getOS = sub {
            return bless {}, 'MockOS';
        };
        *MockOS::ignoredItems = sub { return () };
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
    }
}

use Slim::Utils::Misc qw(msg);

# Mock some main:: constants if needed
{
    no strict 'refs';
    ${"main::DEBUGLOG"} = 0;
}

subtest 'msg' => sub {
    # This is hard to test directly without capturing output, 
    # but we can verify it doesn't crash.
    ok(defined(&msg), 'msg function is defined');
    
    # Simple call test
    eval { msg("Test message\n") };
    ok(!$@, 'msg call did not die: $@');
};

done_testing();
