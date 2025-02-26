// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import "./Strategy.sol";

contract LevCompFactory {
    address public immutable original;

    event Cloned(address indexed clone);
    event Deployed(address indexed original);

    constructor(
        address _vault,
        address _cToken,
        address _router, 
        address _comp, 
        address _comptroller, 
        address _weth,
        uint256 _secondsPerBlock
    ) public {
        Strategy _original = new Strategy(_vault, _cToken, _router, _comp, _comptroller, _weth, _secondsPerBlock);
        emit Deployed(address(_original));

        original = address(_original);
        _original.setStrategist(msg.sender);
    }

    function name() external view returns (string memory) {
        return string(abi.encodePacked("Factory", Strategy(payable(original)).name(), "@", Strategy(payable(original)).apiVersion()));
    }

    function cloneLevComp(
        address _vault,
        address _cToken,
        address _router, 
        address _comp, 
        address _comptroller, 
        address _weth,
        uint256 _secondsPerBlock
    ) external returns (address payable newStrategy) {
        // Copied from https://github.com/optionality/clone-factory/blob/master/contracts/CloneFactory.sol
        bytes20 addressBytes = bytes20(original);
        assembly {
            // EIP-1167 bytecode
            let clone_code := mload(0x40)
            mstore(
                clone_code,
                0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000000000000000000000
            )
            mstore(add(clone_code, 0x14), addressBytes)
            mstore(
                add(clone_code, 0x28),
                0x5af43d82803e903d91602b57fd5bf30000000000000000000000000000000000
            )
            newStrategy := create(0, clone_code, 0x37)
        }

        Strategy(newStrategy).initialize(_vault, _cToken, _router, _comp, _comptroller, _weth, _secondsPerBlock);
        Strategy(newStrategy).setRewards(msg.sender);
        Strategy(newStrategy).setStrategist(msg.sender);
    
        emit Cloned(newStrategy);
    }
}
