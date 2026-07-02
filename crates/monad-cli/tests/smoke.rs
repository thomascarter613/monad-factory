//! Smoke tests for the compiled `monad` binary.

use assert_cmd::Command;
use predicates::str::contains;

fn monad() -> Command {
    Command::new(env!("CARGO_BIN_EXE_monad"))
}

#[test]
fn help_command_works() {
    monad()
        .arg("--help")
        .assert()
        .success()
        .stdout(contains("Monad Factory CLI"))
        .stdout(contains("Usage:"))
        .stdout(contains("Core commands:"))
        .stdout(contains("Foundation command groups:"))
        .stdout(contains("monad doctor"))
        .stdout(contains("monad check"))
        .stdout(contains("monad inspect"))
        .stdout(contains("monad graph"))
        .stdout(contains("monad context"))
        .stdout(contains("monad memory"));
}

#[test]
fn version_command_works() {
    monad().arg("version").assert().success();
}

#[test]
fn info_command_works() {
    monad().arg("info").assert().success();
}

#[test]
fn doctor_works() {
    monad().arg("doctor").assert().success();
}

#[test]
fn check_command_works() {
    monad().arg("check").assert().success();
}

#[test]
fn inspect_command_works() {
    monad().arg("inspect").assert().success();
}

#[test]
fn graph_command_works() {
    monad().arg("graph").assert().success();
}

#[test]
fn list_commands_works() {
    monad()
        .args(["list", "commands"])
        .assert()
        .success()
        .stdout(contains("Monad CLI command catalog"))
        .stdout(contains("monad help"))
        .stdout(contains("monad doctor"))
        .stdout(contains("monad add"))
        .stdout(contains("monad generate"));
}

#[test]
fn list_current_commands_works() {
    monad()
        .args(["list", "current"])
        .assert()
        .success()
        .stdout(contains("Current Monad CLI commands"))
        .stdout(contains("monad doctor"))
        .stdout(contains("monad check"));
}

#[test]
fn list_planned_commands_works() {
    monad()
        .args(["list", "planned"])
        .assert()
        .success()
        .stdout(contains("Planned Monad CLI commands"))
        .stdout(contains("monad new"))
        .stdout(contains("monad add"))
        .stdout(contains("monad ci"));
}
